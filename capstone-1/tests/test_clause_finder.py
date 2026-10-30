"""Unit tests for the Policy Clause Finder.  Run:  python -m unittest discover -s tests -v"""
import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from embed import ConceptEmbedder, stem, tokenize  # noqa: E402
from finder import THRESHOLD, ClauseFinder, load_clauses, main  # noqa: E402
from rank import cosine_similarity, dot, euclidean_distance, norm, rank  # noqa: E402
from verify import best_snippet, split_sentences, verify_quote  # noqa: E402

QUESTIONS = json.loads((ROOT / "data" / "test_questions.json").read_text(encoding="utf-8"))


class HandWrittenMaths(unittest.TestCase):
    def test_dot_and_norm(self):
        self.assertEqual(dot([1, 2, 3], [4, 5, 6]), 32)
        self.assertEqual(norm([3, 4]), 5)

    def test_cosine_known_values(self):
        self.assertAlmostEqual(cosine_similarity([1, 0], [0, 1]), 0.0)
        self.assertAlmostEqual(cosine_similarity([2, 2], [5, 5]), 1.0)      # same direction, any length
        self.assertAlmostEqual(cosine_similarity([1, 2, 3], [4, 5, 6]), 32 / (math.sqrt(14) * math.sqrt(77)))

    def test_euclidean(self):
        self.assertEqual(euclidean_distance([0, 0], [3, 4]), 5)

    def test_errors(self):
        with self.assertRaises(ValueError):
            cosine_similarity([0, 0], [1, 1])
        with self.assertRaises(ValueError):
            dot([1, 2], [1, 2, 3])
        with self.assertRaises(ValueError):
            rank([1.0], [("a", [1.0])], metric="manhattan")

    def test_matches_numpy_to_3dp_on_real_vectors(self):
        finder = ClauseFinder()
        q = finder.embedder.embed(QUESTIONS["questions"][0]["question"])
        for _, vec in finder.vectors:
            lib = float(np.dot(q, vec) / (np.linalg.norm(q) * np.linalg.norm(vec)))
            self.assertEqual(round(cosine_similarity(q, vec), 3), round(lib, 3))

    def test_rank_orders_and_keeps_ties_stable(self):
        items = [("a", [1.0, 0.0]), ("b", [0.0, 1.0]), ("c", [1.0, 0.0])]
        self.assertEqual([i for i, _ in rank([1.0, 0.0], items)], ["a", "c", "b"])
        self.assertEqual([i for i, _ in rank([1.0, 0.0], items, metric="euclidean")], ["a", "c", "b"])
        self.assertEqual(rank([0.0, 0.0], items), [])           # nothing recognised -> nothing ranked


class Embedder(unittest.TestCase):
    def test_stemming_joins_word_forms(self):
        self.assertEqual(stem("charged"), stem("charges"))
        self.assertEqual(stem("charge"), stem("charged"))
        self.assertEqual(stem("address"), stem("addresses"))

    def test_contractions(self):
        self.assertIn("cannot", tokenize("I can't pay"))
        self.assertEqual(tokenize("didn't"), ["did", "not"])

    def test_synonyms_share_a_concept_without_sharing_words(self):
        e = ConceptEmbedder()
        a, b = e.embed("cannot pay my EMI"), e.embed("repayment default")
        self.assertGreater(cosine_similarity(a, b), 0.5)

    def test_longest_phrase_wins(self):
        concepts = [c for _, c in ConceptEmbedder().concepts_found("I lost my job")]
        self.assertIn("hardship", concepts)
        self.assertNotIn("lost_stolen", concepts)


class Verifier(unittest.TestCase):
    TEXT = "The card is blocked immediately. A replacement card is sent within 5 working days."

    def test_verbatim_quote_passes(self):
        self.assertTrue(verify_quote("A replacement card is sent within 5 working days.", self.TEXT))

    def test_altered_or_invented_quote_fails(self):
        self.assertFalse(verify_quote("A replacement card is sent within 2 working days.", self.TEXT))
        self.assertFalse(verify_quote("The card is blocked  immediately.", self.TEXT))   # extra space
        self.assertFalse(verify_quote("", self.TEXT))

    def test_sentences_are_cut_from_the_original(self):
        for s in split_sentences(self.TEXT):
            self.assertIn(s, self.TEXT)

    def test_best_snippet_picks_the_relevant_sentence(self):
        e = ConceptEmbedder()
        snippet = best_snippet(e.embed("how many working days until the replacement arrives"), self.TEXT, e.embed)
        self.assertIn("replacement", snippet)


class ClauseStore(unittest.TestCase):
    def test_store_size_and_fields(self):
        clauses = load_clauses()
        self.assertTrue(15 <= len(clauses) <= 20)
        self.assertEqual(len({c["id"] for c in clauses}), len(clauses))
        self.assertEqual({c["category"] for c in clauses} >= {"loans", "cards", "complaints", "kyc"}, True)

    def test_at_least_three_near_duplicate_pairs(self):
        clauses = load_clauses()
        ids = {c["id"] for c in clauses}
        pairs = {tuple(sorted((c["id"], c["near_duplicate_of"]))) for c in clauses if c.get("near_duplicate_of")}
        self.assertGreaterEqual(len(pairs), 3)
        for a, b in pairs:
            self.assertIn(a, ids)
            self.assertIn(b, ids)

    def test_duplicate_id_is_rejected(self):
        path = ROOT / "results" / "_tmp_dup.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps([{"id": "X", "title": "t", "text": "a"}, {"id": "X", "title": "t", "text": "b"}]))
        try:
            with self.assertRaises(ValueError):
                load_clauses(path)
        finally:
            path.unlink()


class FinderEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.finder = ClauseFinder()

    def test_top3_have_id_score_and_verified_quote(self):
        answer = self.finder.search("Customer cannot pay their EMI")
        self.assertEqual(answer["status"], "found")
        self.assertEqual(len(answer["results"]), 3)
        scores = [r["score"] for r in answer["results"]]
        self.assertEqual(scores, sorted(scores, reverse=True))
        for r in answer["results"]:
            self.assertTrue(r["quote_verified"])
            self.assertIn(r["quote"], self.finder.by_id[r["id"]]["text"])

    def test_every_quote_for_every_test_question_is_verbatim(self):
        sets = QUESTIONS["questions"] + QUESTIONS["stress_set"] + QUESTIONS["out_of_scope"]
        for q in sets:
            for r in self.finder.search(q["question"])["results"]:
                self.assertIn(r["quote"], self.finder.by_id[r["id"]]["text"], q["id"])

    def test_out_of_scope_is_not_found(self):
        for q in QUESTIONS["out_of_scope"]:
            self.assertEqual(self.finder.search(q["question"])["status"], "not_found", q["id"])

    def test_gibberish_is_not_found(self):
        self.assertEqual(self.finder.search("the and of")["status"], "not_found")

    def test_threshold_is_applied(self):
        strict = ClauseFinder(threshold=0.99)
        self.assertEqual(strict.search("Customer cannot pay their EMI")["status"], "not_found")
        self.assertLess(THRESHOLD, 1.0)

    def test_cli_runs(self):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(main(["I", "cannot", "pay", "my", "EMI"]), 0)
        self.assertIn("LN-01", buf.getvalue())
        self.assertIn("verified", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
