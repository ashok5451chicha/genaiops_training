"""
test_mine.py - tests for MY functions in my_vector_math.py (Prompt 4 + Task B).

    python -m unittest test_mine -v
"""
import math
import unittest

import my_vector_math as m

WORDS = {  # from data/vectors.json
    "loan": [5, 1, 2, 2], "mortgage": [5, 1, 3, 1], "overdraft": [4, 2, 1, 3],
    "fraud": [0, 5, 2, 1], "KYC": [1, 1, 5, 1], "complaint": [0, 1, 0, 5],
}


class FourFunctions(unittest.TestCase):
    """Prompt 4: five test cases including edge cases."""

    def test_worked_example(self):
        self.assertEqual(m.dot([3, 4], [4, 3]), 24)
        self.assertEqual(m.norm([3, 4]), 5)
        self.assertAlmostEqual(m.cosine_similarity([3, 4], [4, 3]), 0.96)
        self.assertAlmostEqual(m.euclidean_distance([3, 4], [4, 3]), math.sqrt(2))

    def test_zero_vector_has_no_cosine(self):
        with self.assertRaises(ValueError):
            m.cosine_similarity([0, 0], [1, 2])
        self.assertEqual(m.norm([0, 0, 0]), 0)

    def test_different_lengths_rejected_everywhere(self):
        for f in (m.dot, m.cosine_similarity, m.euclidean_distance):
            with self.subTest(f.__name__), self.assertRaises(ValueError):
                f([1, 2], [1, 2, 3])

    def test_negative_numbers_and_opposite_direction(self):
        self.assertAlmostEqual(m.cosine_similarity([1, 2, 3], [-1, -2, -3]), -1.0)
        self.assertAlmostEqual(m.euclidean_distance([-1, -1], [2, 3]), 5.0)

    def test_same_direction_different_length(self):
        self.assertAlmostEqual(m.cosine_similarity([3, 4], [6, 8]), 1.0)
        self.assertAlmostEqual(m.euclidean_distance([3, 4], [6, 8]), 5.0)


class Nearest(unittest.TestCase):
    """Task B: nearest(query, candidates, metric)."""

    def test_cosine_full_order(self):
        # Exact order, not just "the right length": a test that only checks len() could never catch a wrong sort.
        # Checked by hand: complaint 11/(5.831*5.099)=0.370 beats fraud 11/(5.831*5.477)=0.344.
        # (My first version of this test had fraud before complaint - the test was wrong, not the code.)
        self.assertEqual(m.nearest(WORDS["loan"], {k: v for k, v in WORDS.items() if k != "loan"}),
                         ["mortgage", "overdraft", "KYC", "complaint", "fraud"])

    def test_euclidean_lower_is_better(self):
        cands = {"far": [10, 10], "near": [1, 1], "middle": [4, 4]}
        self.assertEqual(m.nearest([0, 0.5], cands, metric="euclidean"), ["near", "middle", "far"])

    def test_metrics_can_disagree(self):
        # Same direction but much longer: cosine says identical, distance says far away.
        cands = {"long, same direction": [30, 40], "short, nearby": [4, 2]}
        self.assertEqual(m.nearest([3, 4], cands, "cosine")[0], "long, same direction")
        self.assertEqual(m.nearest([3, 4], cands, "euclidean")[0], "short, nearby")

    def test_ties_keep_input_order(self):
        cands = {"b": [2, 0], "a": [1, 0], "c": [0, 1]}   # b and a have the same direction -> cosine tie
        self.assertEqual(m.nearest([5, 0], cands), ["b", "a", "c"])

    def test_empty_candidates(self):
        self.assertEqual(m.nearest([1, 2], {}), [])

    def test_unknown_metric_is_rejected(self):
        # Found in review of version 1: any metric that was not exactly "cosine" was silently treated as euclidean.
        for bad in ("Cosine", "manhattan", "euclidian"):
            with self.subTest(bad), self.assertRaises(ValueError):
                m.nearest([1, 2], {"x": [1, 2]}, metric=bad)

    def test_zero_vector_candidate_names_the_culprit(self):
        with self.assertRaises(ValueError) as ctx:
            m.nearest([1, 2], {"good": [1, 1], "empty profile": [0, 0]})
        self.assertIn("empty profile", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
