"""
kyc_pipeline.py - the KYC remediation logic. Two jobs, both built on vector closeness:

  A. CLASSIFY  each analyst note into a remediation category (nearest category vector, by cosine similarity)
  B. DETECT    probable duplicate customer profiles (name + address + occupation vectors that are very close)

Safety rules built in: IDs are masked in every output, an empty note goes to a person, and a probable duplicate is
NEVER merged automatically - it goes to a human review queue.
"""
import csv
import json
from pathlib import Path

from embedder import embed
from vector_math import cosine_similarity, euclidean_distance

ROOT = Path(__file__).resolve().parent


def load_json(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def load_config():
    return json.loads((ROOT / "config.json").read_text(encoding="utf-8"))


def mask_id(id_number, visible=3):
    """SYNID-48213 -> SYNID-**213 : only the last `visible` characters of the number stay readable.

    The prefix is everything up to and including the last '-' (no '-' means no prefix). A number that is not longer
    than `visible` is masked completely: showing all of it would reveal the whole ID.
    """
    text = str(id_number or "")
    prefix, _, number = text.rpartition("-")
    prefix = prefix + "-" if prefix else ""
    if len(number) <= visible:
        return prefix + "*" * len(number)                            # too short: hide every character
    return prefix + "*" * (len(number) - visible) + number[-visible:]   # hide all but the last `visible`


def category_vectors(categories, bucket_weight):
    return {c["code"]: embed(c["description"], bucket_weight) for c in categories}


def classify_note(note, cat_vectors, bucket_weight=0.5, min_score=0.30):
    """Return (category_code, score). Highest cosine similarity wins. Empty or weak notes go to MANUAL_REVIEW."""
    vec = embed(note, bucket_weight)
    if not any(vec):
        return "MANUAL_REVIEW", 0.0
    best_code, best_score = max(((code, cosine_similarity(vec, v)) for code, v in cat_vectors.items()), key=lambda s: s[1])
    if best_score < min_score:
        return "MANUAL_REVIEW", best_score
    return best_code, best_score


def profile_text(rec):
    return f"{rec['name']} {rec['address']} {rec['occupation']}"


def find_duplicates(records, bucket_weight=0.5, duplicate_cosine=0.85, review_cosine=0.70):
    """Compare every pair ONCE (i < j). Returns a list of dicts for pairs at or above review_cosine."""
    vecs = [embed(profile_text(r), bucket_weight) for r in records]
    pairs = []
    for i in range(len(records)):
        for j in range(i + 1, len(records)):   # j > i: every pair once, never a record with itself
            cos = cosine_similarity(vecs[i], vecs[j])
            if cos >= review_cosine:
                decision = "PROBABLE_DUPLICATE_HUMAN_REVIEW" if cos >= duplicate_cosine else "POSSIBLE_DUPLICATE_HUMAN_REVIEW"
                pairs.append(dict(record_a=records[i]["record_id"], record_b=records[j]["record_id"], cosine=round(cos, 3),
                                  euclidean=round(euclidean_distance(vecs[i], vecs[j]), 3), decision=decision))
    return sorted(pairs, key=lambda p: -p["cosine"])


def build_queue(records, categories, cfg):
    cats = {c["code"]: c for c in categories}
    cvec = category_vectors(categories, cfg["bucket_weight"])
    rows = []
    for r in records:
        code, score = classify_note(r["analyst_note"], cvec, cfg["bucket_weight"], cfg["min_note_score"])
        c = cats.get(code)
        rows.append(dict(record_id=r["record_id"], customer_ref=r["customer_ref"], masked_id=mask_id(r["id_number"], cfg["mask_visible_chars"]),
                         category=code, score=round(score, 3), priority=c["priority"] if c else "HIGH",
                         action=c["action"] if c else "Analyst reads the record and decides (empty or unclear note)",
                         expected=r.get("expected_category", "")))
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return sorted(rows, key=lambda x: (order[x["priority"]], -x["score"]))


def evaluate(queue, dup_pairs, gold):
    correct = sum(1 for q in queue if q["category"] == q["expected"])
    found = {tuple(sorted((p["record_a"], p["record_b"]))) for p in dup_pairs if p["decision"].startswith("PROBABLE")}
    truth = {tuple(sorted(p)) for p in gold["duplicate_pairs"]}
    tp = len(found & truth)
    in_review = {tuple(sorted((p["record_a"], p["record_b"]))) for p in dup_pairs}
    return dict(classified_correct=correct, total=len(queue), accuracy=round(correct / len(queue), 3),
                dup_true_positive=tp, dup_false_positive=len(found - truth), dup_missed=len(truth - found),
                dup_precision=round(tp / len(found), 3) if found else 0.0, dup_recall=round(tp / len(truth), 3),
                dup_recall_incl_possible=round(len(in_review & truth) / len(truth), 3))


def write_csv(path, rows, fieldnames=None):
    """Write a list of dicts to a CSV file: header from the dict keys, one line per dict. Creates the folder."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = fieldnames or (list(rows[0]) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path
