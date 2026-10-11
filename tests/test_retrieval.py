import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from researchpilot.retrieval import search_chunks


class TestSearchChunks(unittest.TestCase):

    def setUp(self):
        self.chunks = [
            {"page_number": 1, "text": "ResearchPilot helps with research."},
            {"page_number": 2, "text": "Python processes documents."},
            {"page_number": 3, "text": "The research project uses Python."},
        ]

    def test_finds_matching_chunks(self):
        results = search_chunks("research", self.chunks)
        self.assertGreater(len(results), 0)
        self.assertTrue(
            all("research" in item["text"].lower() for item in results)
        )

    def test_best_match_comes_first(self):
        results = search_chunks("research project", self.chunks)
        self.assertEqual(results[0]["page_number"], 3)
        self.assertEqual(results[0]["score"], 2)

    def test_empty_query_returns_no_results(self):
        self.assertEqual(search_chunks("", self.chunks), [])


if __name__ == "__main__":
    unittest.main()
