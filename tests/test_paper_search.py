"""Tests for searching complete PDF research papers."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Make the src folder available so Python can import ResearchPilot.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from researchpilot.paper_search import search_pdf


class TestPaperSearch(unittest.TestCase):
    """Test the paper-search workflow without needing real PDFs or AI models."""

    def test_blank_question_returns_no_results(self):
        # A blank question should return immediately.
        # The PDF pipeline must not be called in this case.
        with patch("researchpilot.paper_search.process_pdf") as mock_process:
            results = search_pdf("example.pdf", "   ")

        self.assertEqual(results, [])
        mock_process.assert_not_called()

    def test_invalid_top_k_raises_error(self):
        # Asking for zero results is invalid.
        # The function should reject it before processing the PDF.
        with self.assertRaises(ValueError):
            search_pdf("example.pdf", "What was discovered?", top_k=0)

    def test_empty_pdf_chunks_return_no_results(self):
        # Imagine the PDF contains no extractable text.
        # There is nothing to index or search.
        with patch(
            "researchpilot.paper_search.process_pdf",
            return_value=[],
        ), patch(
            "researchpilot.paper_search.build_vector_index",
        ) as mock_build:
            results = search_pdf("example.pdf", "What was discovered?")

        self.assertEqual(results, [])
        mock_build.assert_not_called()

    def test_search_returns_matching_passage(self):
        # Simulate one chunk extracted from page 4 of a research paper.
        chunks = [
            {
                "page_number": 4,
                "text": "The experiment improved model accuracy.",
            }
        ]

        # Simulate a search result from the vector-search function.
        expected_results = [
            {
                "page_number": 4,
                "text": "The experiment improved model accuracy.",
                "score": 0.91,
            }
        ]

        # Replace the expensive PDF and AI operations with predictable
        # test doubles. This makes the test fast and repeatable.
        with patch(
            "researchpilot.paper_search.process_pdf",
            return_value=chunks,
        ), patch(
            "researchpilot.paper_search.build_vector_index",
            return_value="fake-index",
        ), patch(
            "researchpilot.paper_search.search_vector_index",
            return_value=expected_results,
        ) as mock_search:
            results = search_pdf(
                "example.pdf",
                "Did the experiment improve accuracy?",
                top_k=1,
            )

        # Confirm that the result is returned with its source page.
        self.assertEqual(results, expected_results)
        self.assertEqual(results[0]["page_number"], 4)

        # Confirm that our question and requested result count were passed on.
        mock_search.assert_called_once_with(
            query="Did the experiment improve accuracy?",
            chunks=chunks,
            index="fake-index",
            top_k=1,
        )


if __name__ == "__main__":
    # Run these tests when this file is executed directly.
    unittest.main()
