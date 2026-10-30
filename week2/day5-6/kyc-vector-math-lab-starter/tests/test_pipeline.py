"""Tests for kyc_pipeline.py and run_pipeline.py (missing piece M6): masking, classification, duplicates,
end-to-end quality and data hygiene."""
import contextlib
import csv
import io
import re
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import run_pipeline  # noqa: E402
from kyc_pipeline import (build_queue, category_vectors, classify_note, evaluate, find_duplicates,  # noqa: E402
                          load_config, load_json, mask_id, write_csv)

RECORDS = load_json("kyc_records.json")
CATEGORIES = load_json("remediation_categories.json")
GOLD = load_json("gold_duplicates.json")
CFG = load_config()


class MaskId(unittest.TestCase):
    def test_keeps_prefix_and_last_three(self):
        self.assertEqual(mask_id("SYNID-48213"), "SYNID-**213")

    def test_visible_count_is_respected(self):
        self.assertEqual(mask_id("SYNID-48213", visible=2), "SYNID-***13")

    def test_short_number_fully_masked(self):
        self.assertEqual(mask_id("SYNID-12"), "SYNID-**")
        self.assertEqual(mask_id("SYNID-123"), "SYNID-***")     # exactly `visible` long: showing it would reveal all

    def test_no_prefix(self):
        self.assertEqual(mask_id("9876543"), "****543")

    def test_empty(self):
        self.assertEqual(mask_id(""), "")
        self.assertEqual(mask_id(None), "")

    def test_raw_digits_never_survive(self):
        for r in RECORDS:
            number = r["id_number"].split("-")[-1]
            self.assertNotIn(number, mask_id(r["id_number"], CFG["mask_visible_chars"]))


class ClassifyNote(unittest.TestCase):
    CVEC = category_vectors(CATEGORIES, CFG["bucket_weight"])

    def classify(self, note):
        return classify_note(note, self.CVEC, CFG["bucket_weight"], CFG["min_note_score"])

    def test_empty_note_goes_to_manual_review(self):
        self.assertEqual(self.classify(""), ("MANUAL_REVIEW", 0.0))

    def test_highest_cosine_wins(self):
        self.assertEqual(self.classify("utility bill for the residence has expired")[0], "PROOF_OF_ADDRESS")
        self.assertEqual(self.classify("passport name spelling differs")[0], "ID_MISMATCH")
        self.assertEqual(self.classify("politically exposed person with offshore remittance")[0], "HIGH_RISK_REVIEW")

    def test_weak_note_goes_to_manual_review(self):
        code, score = self.classify("customer called about the weather")
        self.assertEqual(code, "MANUAL_REVIEW")
        self.assertLess(score, CFG["min_note_score"])

    def test_score_is_between_0_and_1(self):
        for r in RECORDS:
            _, score = self.classify(r["analyst_note"])
            self.assertTrue(0.0 <= score <= 1.0)


class FindDuplicates(unittest.TestCase):
    PAIRS = find_duplicates(RECORDS, CFG["bucket_weight"], CFG["duplicate_cosine"], CFG["review_cosine"])

    def test_a_record_is_never_its_own_duplicate(self):
        for p in self.PAIRS:
            self.assertNotEqual(p["record_a"], p["record_b"])

    def test_every_pair_reported_once(self):
        keys = [tuple(sorted((p["record_a"], p["record_b"]))) for p in self.PAIRS]
        self.assertEqual(len(keys), len(set(keys)))

    def test_decisions_follow_thresholds_and_always_need_a_human(self):
        for p in self.PAIRS:
            self.assertGreaterEqual(p["cosine"], CFG["review_cosine"])
            expected = "PROBABLE" if p["cosine"] >= CFG["duplicate_cosine"] else "POSSIBLE"
            self.assertTrue(p["decision"].startswith(expected))
            self.assertTrue(p["decision"].endswith("HUMAN_REVIEW"))

    def test_sorted_by_cosine(self):
        scores = [p["cosine"] for p in self.PAIRS]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_identical_profiles_score_one(self):
        twin = [dict(RECORDS[0]), dict(RECORDS[0], record_id="KX")]
        pairs = find_duplicates(twin)
        self.assertEqual(len(pairs), 1)
        self.assertAlmostEqual(pairs[0]["cosine"], 1.0)


class EndToEndQuality(unittest.TestCase):
    """Honest quality bar on the 20 synthetic records (measured, see README: Results)."""

    def setUp(self):
        self.queue = build_queue(RECORDS, CATEGORIES, CFG)
        self.pairs = find_duplicates(RECORDS, CFG["bucket_weight"], CFG["duplicate_cosine"], CFG["review_cosine"])
        self.result = evaluate(self.queue, self.pairs, GOLD)

    def test_classification_accuracy(self):
        self.assertGreaterEqual(self.result["accuracy"], 0.9)

    def test_no_false_probable_duplicates(self):
        self.assertEqual(self.result["dup_false_positive"], 0)

    def test_every_known_duplicate_reaches_a_human(self):
        self.assertEqual(self.result["dup_recall_incl_possible"], 1.0)

    def test_queue_is_sorted_by_priority(self):
        order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        ranks = [order[q["priority"]] for q in self.queue]
        self.assertEqual(ranks, sorted(ranks))

    def test_queue_ids_are_masked(self):
        for q, r in zip(sorted(self.queue, key=lambda q: q["record_id"]), sorted(RECORDS, key=lambda r: r["record_id"])):
            self.assertEqual(q["masked_id"], mask_id(r["id_number"], CFG["mask_visible_chars"]))

    def test_run_pipeline_writes_three_files_without_raw_ids(self):
        tmp = Path(tempfile.mkdtemp())
        old = run_pipeline.OUT
        run_pipeline.OUT = tmp
        try:
            with contextlib.redirect_stdout(io.StringIO()) as screen:
                self.assertEqual(run_pipeline.main(), 0)
            names = {"remediation_queue.csv", "duplicate_pairs.csv", "summary.md"}
            self.assertEqual({f.name for f in tmp.iterdir()}, names)
            texts = [screen.getvalue()] + [(tmp / n).read_text(encoding="utf-8") for n in names]
            for r in RECORDS:
                for t in texts:
                    self.assertNotIn(r["id_number"], t)
        finally:
            run_pipeline.OUT = old
            shutil.rmtree(tmp)

    def test_write_csv_round_trip(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            path = write_csv(tmp / "sub" / "x.csv", [{"a": 1, "b": "two"}, {"a": 3, "b": "four"}])
            with path.open(encoding="utf-8") as f:
                self.assertEqual(list(csv.DictReader(f)), [{"a": "1", "b": "two"}, {"a": "3", "b": "four"}])
        finally:
            shutil.rmtree(tmp)


class DataHygiene(unittest.TestCase):
    def test_record_ids_unique(self):
        ids = [r["record_id"] for r in RECORDS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_customer_refs_unique(self):
        refs = [r["customer_ref"] for r in RECORDS]
        self.assertEqual(len(refs), len(set(refs)))

    def test_dates_are_iso_and_not_in_the_future(self):
        for r in RECORDS:
            self.assertRegex(r["last_review"], r"^\d{4}-\d{2}-\d{2}$", r["record_id"])
            self.assertLessEqual(date.fromisoformat(r["last_review"]), date.today(), r["record_id"])

    def test_status_values(self):
        for r in RECORDS:
            self.assertIn(r["status"], {"active", "dormant"}, r["record_id"])

    def test_expected_categories_exist(self):
        codes = {c["code"] for c in CATEGORIES} | {"MANUAL_REVIEW"}
        for r in RECORDS:
            self.assertIn(r["expected_category"], codes, r["record_id"])

    def test_gold_pairs_refer_to_real_records(self):
        ids = {r["record_id"] for r in RECORDS}
        for a, b in GOLD["duplicate_pairs"]:
            self.assertIn(a, ids)
            self.assertIn(b, ids)

    def test_ids_are_synthetic(self):
        for r in RECORDS:
            self.assertTrue(re.fullmatch(r"SYNID-\d{5}", r["id_number"]), r["record_id"])

    def test_config_thresholds_are_consistent(self):
        self.assertLess(CFG["review_cosine"], CFG["duplicate_cosine"])
        for key in ("review_cosine", "duplicate_cosine", "min_note_score"):
            self.assertTrue(0.0 <= CFG[key] <= 1.0, key)


if __name__ == "__main__":
    unittest.main()
