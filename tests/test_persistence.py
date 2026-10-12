"""Tests for saving and loading ResearchPilot search data."""

import tempfile
import unittest
from pathlib import Path

import faiss
import numpy as np

from researchpilot.persistence import save_search_data, load_search_data


class TestPersistence(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_dir = Path(self.temp_dir.name)

        # Create a tiny FAISS index without loading an AI model.
        self.index = faiss.IndexFlatIP(2)
        vectors = np.array(
            [[1.0, 0.0], [0.0, 1.0]],
            dtype="float32",
        )
        self.index.add(vectors)

        self.chunks = [
            {
                "page_number": 1,
                "text": "First research passage.",
            },
            {
                "page_number": 2,
                "text": "Second research passage.",
            },
        ]

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_preserves_chunks(self):
        save_search_data(self.index, self.chunks, self.storage_dir)

        loaded_index, loaded_chunks = load_search_data(self.storage_dir)

        self.assertEqual(loaded_index.ntotal, 2)
        self.assertEqual(loaded_chunks, self.chunks)

    def test_save_creates_storage_directory(self):
        new_dir = self.storage_dir / "nested" / "library"

        save_search_data(self.index, self.chunks, new_dir)

        self.assertTrue((new_dir / "index.faiss").is_file())
        self.assertTrue((new_dir / "chunks.json").is_file())

    def test_save_rejects_mismatched_vector_and_chunk_counts(self):
        with self.assertRaises(ValueError):
            save_search_data(self.index, self.chunks[:1], self.storage_dir)

    def test_load_fails_when_files_are_missing(self):
        with self.assertRaises(FileNotFoundError):
            load_search_data(self.storage_dir)

    def test_load_rejects_mismatched_saved_chunk_count(self):
        save_search_data(self.index, self.chunks, self.storage_dir)

        # Simulate damaged or inconsistent metadata.
        import json

        chunks_path = self.storage_dir / "chunks.json"
        with chunks_path.open("w", encoding="utf-8") as file:
            json.dump(self.chunks[:1], file)

        with self.assertRaises(ValueError):
            load_search_data(self.storage_dir)


if __name__ == "__main__":
    unittest.main()
