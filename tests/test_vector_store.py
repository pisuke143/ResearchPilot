"""Tests for ResearchPilot's vector storage and search."""

import sys
import unittest
from pathlib import Path

# Add the project's src folder to Python's module search path.
# This lets the tests import ResearchPilot modules without installing the project.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from researchpilot.vector_store import (
    build_vector_index,
    search_vector_index,
)


class TestVectorStore(unittest.TestCase):

    def test_building_index_with_no_chunks_fails(self):
        # An index needs at least one passage to search.
        with self.assertRaises(ValueError):
            build_vector_index([])

    def test_search_with_no_chunks_returns_empty_list(self):
        # With no passages, there is nothing to return.
        # The function should exit before loading the AI model.
        self.assertEqual(search_vector_index("research", [], None), [])

    def test_invalid_top_k_fails(self):
        # top_k tells the search how many results we want.
        # Zero is invalid because we need at least one result.
        with self.assertRaises(ValueError):
            search_vector_index("research", [], None, top_k=0)


if __name__ == "__main__":
    # Run these tests when this file is executed directly.
    unittest.main()
