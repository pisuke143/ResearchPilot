import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from researchpilot.semantic_search import semantic_search


class TestSemanticSearch(unittest.TestCase):

    def test_empty_query_returns_no_results(self):
        self.assertEqual(semantic_search("  ", []), [])

    def test_invalid_top_k_raises_error(self):
        with self.assertRaises(ValueError):
            semantic_search("research", [], top_k=0)

    def test_results_include_page_and_score(self):
        chunks = [
            {"page_number": 1, "text": "A scientific study."},
            {"page_number": 2, "text": "Cooking a delicious meal."},
        ]

        class FakeModel:
            def encode(self, texts, convert_to_tensor=True):
                return texts

        fake_scores = torch.tensor([0.9, 0.2])

        with patch(
            "researchpilot.semantic_search.get_embedding_model",
            return_value=FakeModel(),
        ), patch(
            "researchpilot.semantic_search.util.cos_sim",
            return_value=fake_scores.unsqueeze(0),
        ):
            results = semantic_search("scientific research", chunks)

        self.assertEqual(results[0]["page_number"], 1)
        self.assertAlmostEqual(results[0]["score"], 0.9)
        self.assertEqual(results[1]["page_number"], 2)


if __name__ == "__main__":
    unittest.main()
