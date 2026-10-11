import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from researchpilot.text_processing import split_into_chunks


class TestSplitIntoChunks(unittest.TestCase):

    def test_empty_text(self):
        self.assertEqual(split_into_chunks(""), [])

    def test_short_text(self):
        self.assertEqual(
            split_into_chunks("Hello world", 20),
            ["Hello world"]
        )

    def test_chunks_respect_size(self):
        chunks = split_into_chunks("cat dog bird", 7)

        for chunk in chunks:
            self.assertLessEqual(len(chunk), 7)

    def test_words_are_preserved(self):
        text = "cat dog bird"
        chunks = split_into_chunks(text, 7)

        self.assertEqual(" ".join(chunks), text)

    def test_invalid_chunk_size(self):
        with self.assertRaises(ValueError):
            split_into_chunks("hello", 0)


if __name__ == "__main__":
    unittest.main()
