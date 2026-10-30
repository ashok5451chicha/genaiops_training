"""
run_pipeline.py - the end-to-end run:  load -> embed -> classify notes -> find duplicates -> write queues -> report.

    python run_pipeline.py

Outputs (in output/):  remediation_queue.csv   duplicate_pairs.csv   summary.md
Nothing is merged or decided automatically: both queues are for human review. IDs are masked everywhere, and the run
fails loudly if a raw ID number reaches the screen or any output file.
"""
import io
import sys
from contextlib import redirect_stdout

from kyc_pipeline import (ROOT, build_queue, evaluate, find_duplicates, load_config, load_json, write_csv)

OUT = ROOT / "output"


def print_table(rows, columns):
    """Print dicts as a fixed-width text table (column widths from the longest value)."""
    widths = {c: max(len(c), *(len(str(r[c])) for r in rows)) if rows else len(c) for c in columns}
    print("  ".join(c.ljust(widths[c]) for c in columns))
    print("  ".join("-" * widths[c] for c in columns))
    for r in rows:
        print("  ".join(str(r[c]).ljust(widths[c]) for c in columns))


def summary_markdown(cfg, queue, pairs, result):
    lines = [
        "# KYC remediation run - summary",
        "",
        "Synthetic data only. Every item below is for HUMAN REVIEW; nothing was merged or closed automatically.",
        "",
        "## Thresholds used (config.json, owned by the process owner)",
        "",
        f"* duplicate_cosine {cfg['duplicate_cosine']} (probable duplicate) · review_cosine {cfg['review_cosine']} "
        f"(possible duplicate) · min_note_score {cfg['min_note_score']} · mask_visible_chars {cfg['mask_visible_chars']}",
        "",
        "## Job A: classify analyst notes",
        "",
        f"* Correct category: **{result['classified_correct']}/{result['total']}** (accuracy {result['accuracy']})",
        f"* Sent to MANUAL_REVIEW: {sum(q['category'] == 'MANUAL_REVIEW' for q in queue)}",
        "",
        "| record | masked ID | category | score | priority | expected |",
        "|---|---|---|---|---|---|",
        *[f"| {q['record_id']} | {q['masked_id']} | {q['category']} | {q['score']} | {q['priority']} | {q['expected']} |"
          for q in queue],
        "",
        "## Job B: duplicate profiles (human review only)",
        "",
        f"* Probable duplicates: true positives {result['dup_true_positive']}, false positives "
        f"{result['dup_false_positive']}, missed {result['dup_missed']}",
        f"* Precision {result['dup_precision']} · recall {result['dup_recall']} · recall including POSSIBLE "
        f"{result['dup_recall_incl_possible']}",
        "",
        "| record A | record B | cosine | euclidean | decision |",
        "|---|---|---|---|---|",
        *[f"| {p['record_a']} | {p['record_b']} | {p['cosine']} | {p['euclidean']} | {p['decision']} |" for p in pairs],
        "",
    ]
    return "\n".join(lines)


def check_no_raw_ids(records, texts):
    """Privacy guard: no raw ID number may appear on screen or in any output. Returns the leaked IDs."""
    raw = {r["id_number"] for r in records if r.get("id_number")}
    return sorted(i for i in raw if any(i in t for t in texts))


def main():
    cfg = load_config()
    records = load_json("kyc_records.json")
    categories = load_json("remediation_categories.json")
    gold = load_json("gold_duplicates.json")

    screen = io.StringIO()
    with redirect_stdout(screen):
        print(f"Loaded {len(records)} synthetic KYC records, {len(categories)} remediation categories")
        queue = build_queue(records, categories, cfg)                                   # Job A
        pairs = find_duplicates(records, cfg["bucket_weight"], cfg["duplicate_cosine"], cfg["review_cosine"])  # Job B
        result = evaluate(queue, pairs, gold)

        print("\nREMEDIATION QUEUE (sorted by priority, then score)\n")
        print_table(queue, ["record_id", "customer_ref", "masked_id", "category", "score", "priority", "expected"])
        print("\nDUPLICATE CANDIDATES (human review only - nothing is merged)\n")
        if pairs:
            print_table(pairs, ["record_a", "record_b", "cosine", "euclidean", "decision"])
        else:
            print("(none at or above review_cosine)")
        print(f"\nClassification: {result['classified_correct']}/{result['total']} correct (accuracy {result['accuracy']})")
        print(f"Duplicates: precision {result['dup_precision']}, recall {result['dup_recall']}, "
              f"recall incl. possible {result['dup_recall_incl_possible']} "
              f"(TP {result['dup_true_positive']}, FP {result['dup_false_positive']}, missed {result['dup_missed']})")

    files = [
        write_csv(OUT / "remediation_queue.csv", queue),
        write_csv(OUT / "duplicate_pairs.csv", pairs,
                  fieldnames=["record_a", "record_b", "cosine", "euclidean", "decision"]),
    ]
    summary = OUT / "summary.md"
    summary.write_text(summary_markdown(cfg, queue, pairs, result), encoding="utf-8")
    files.append(summary)

    text = screen.getvalue()
    leaked = check_no_raw_ids(records, [text] + [f.read_text(encoding="utf-8") for f in files])
    if leaked:
        for f in files:                 # never leave unmasked files behind
            f.unlink()
        print(f"STOPPED: {len(leaked)} raw ID number(s) would appear in the output. Outputs deleted. "
              "Check that mask_id() is applied.", file=sys.stderr)
        return 1
    print(text, end="")
    print("\nWrote: " + ", ".join(str(f.relative_to(ROOT)) if f.is_relative_to(ROOT) else str(f) for f in files))
    print("Privacy check: no raw ID number on screen or in any output file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
