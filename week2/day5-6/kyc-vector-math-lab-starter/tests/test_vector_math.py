import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from vector_math import cosine_similarity, dot, euclidean_distance, norm, normalize


class VectorMathTests(unittest.TestCase):
    def test_dot(self):
        self.assertEqual(dot([3, 4], [4, 3]), 24)

    def test_norm(self):
        self.assertEqual(norm([3, 4]), 5)

    def test_normalize_has_length_one(self):
        self.assertAlmostEqual(norm(normalize([3, 4])), 1.0)

    def test_cosine_same_direction(self):
        self.assertAlmostEqual(cosine_similarity([3, 4], [6, 8]), 1.0)

    def test_cosine_known_value(self):
        self.assertAlmostEqual(cosine_similarity([1, 0], [1, 1]), 1 / math.sqrt(2))   # 1 / (1 x sqrt 2) = 0.7071, not 0.5

    def test_cosine_right_angle(self):
        self.assertAlmostEqual(cosine_similarity([1, 0], [0, 1]), 0.0)

    def test_cosine_never_above_one(self):
        self.assertLessEqual(cosine_similarity([5, 1, 2], [1, 7, 3]), 1.0)

    def test_euclidean_345(self):
        self.assertEqual(euclidean_distance([0, 0], [3, 4]), 5)

    def test_euclidean_is_not_manhattan(self):
        self.assertAlmostEqual(euclidean_distance([0, 0], [1, 1]), math.sqrt(2))

    def test_zero_vector_is_an_error(self):
        with self.assertRaises(ValueError):
            cosine_similarity([0, 0], [1, 1])
        with self.assertRaises(ValueError):
            cosine_similarity([1, 1], [0, 0])
        with self.assertRaises(ValueError):
            normalize([0, 0, 0])

    def test_brief_example(self):
        # Participant brief section 4: a = (2, 1), b = (1, 2) -> dot 4, cosine 0.8, distance 1.414
        self.assertEqual(dot([2, 1], [1, 2]), 4)
        self.assertAlmostEqual(cosine_similarity([2, 1], [1, 2]), 0.8)
        self.assertAlmostEqual(euclidean_distance([2, 1], [1, 2]), math.sqrt(2))

    def test_different_lengths_are_an_error(self):
        for f in (dot, cosine_similarity, euclidean_distance):
            with self.assertRaises(ValueError):
                f([1, 2], [1, 2, 3])

    def test_distance_unit_vector_identity(self):
        a, b = [3, 4, 1], [1, 2, 5]
        d = euclidean_distance(normalize(a), normalize(b))
        self.assertAlmostEqual(d * d, 2 - 2 * cosine_similarity(a, b))


if __name__ == "__main__":
    unittest.main()
