import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from embedder import embed, tokenize


class EmbedderTests(unittest.TestCase):
    def test_case_does_not_matter(self):
        self.assertEqual(embed("Passport EXPIRED"), embed("passport expired"))

    def test_empty_text_is_zero_vector(self):
        self.assertFalse(any(embed("")))

    def test_stopwords_dropped(self):
        self.assertNotIn("the", tokenize("the bill"))


# Pipeline tests (mask_id, classify_note, find_duplicates, end-to-end quality, data hygiene): tests/test_pipeline.py


if __name__ == "__main__":
    unittest.main()
