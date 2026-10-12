"""Tests for ResearchPilot's vector storage and search."""

import sys
import unittest
from pathlib import Path

# Add the project's src folder to Python's module search path.
# This allows Python to find ResearchPilot without installing it.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# Import the functions we want to test.
from researchpilot.vector_store import (
    build_vector_index,
    search_vector_index,
)


class TestVectorStore(unittest.TestCase):
    """Check that vector indexing and searching behave as expected."""

    def test_building_index_with_no_chunks_fails(self):
        # An index needs at least one passage to search.
        # An empty list should raise a clear error.
        with self.assertRaises(ValueError):
            build_vector_index([])

    def test_search_with_no_chunks_returns_empty_list(self):
        # If there are no passages, there is nothing to search.
        # The function should return an empty list immediately.
        self.assertEqual(
            search_vector_index("research", [], None),
            [],
        )

    def test_invalid_top_k_fails(self):
        # top_k controls how many results we want.
        # Zero is invalid, so the function should raise ValueError.
        with self.assertRaises(ValueError):
            search_vector_index("research", [], None, top_k=0)

    def test_vector_search_returns_relevant_passage(self):
        # Create two sample passages, as if they came from a research paper.
        # Each passage includes a page number for source tracking.
        chunks = [
            {
                "page_number": 1,
                "text": "Cats and dogs are common household pets.",
            },
            {
                "page_number": 2,
                "text": "Neural networks learn patterns from training data.",
            },
        ]

        # Convert the passages into embeddings and add them to a FAISS index.
        index = build_vector_index(chunks)

        # Search for a question related to neural networks.
        # top_k=1 means we want only the single closest match.
        results = search_vector_index(
            query="How do neural networks learn?",
            chunks=chunks,
            index=index,
            top_k=1,
        )

        # Check that the search returned exactly one result.
        self.assertEqual(len(results), 1)

        # Check that the neural-network passage was ranked first.
        self.assertEqual(results[0]["page_number"], 2)

        # Check that the result includes a similarity score.
        self.assertIn("score", results[0])


if __name__ == "__main__":
    # Run this test file directly if we execute it as a script.
    unittest.main()
