"""Save and load ResearchPilot search indexes and their source chunks."""

import json
import os
from pathlib import Path

import faiss


def save_search_data(index, chunks: list[dict], storage_dir: str | Path) -> None:
    """Save a FAISS index and its matching chunks to disk."""

    # Each vector must correspond to exactly one chunk.
    if index.ntotal != len(chunks):
        raise ValueError(
            "The number of indexed vectors must match the number of chunks"
        )

    # Create the storage folder if it does not already exist.
    storage_path = Path(storage_dir)
    storage_path.mkdir(parents=True, exist_ok=True)

    # Write temporary files first, so incomplete writes are less likely
    # to replace the currently saved files.
    index_temp = storage_path / "index.faiss.tmp"
    chunks_temp = storage_path / "chunks.json.tmp"

    try:
        # Save the FAISS index.
        faiss.write_index(index, str(index_temp))

        # Save the original chunk text and its metadata.
        with chunks_temp.open("w", encoding="utf-8") as file:
            json.dump(chunks, file, ensure_ascii=False, indent=2)

        # Replace the saved files with the new versions.
        # Loading will check that both files still match.
        os.replace(chunks_temp, storage_path / "chunks.json")
        os.replace(index_temp, storage_path / "index.faiss")

    finally:
        # Remove leftover temporary files after a failure.
        index_temp.unlink(missing_ok=True)
        chunks_temp.unlink(missing_ok=True)


def load_search_data(storage_dir: str | Path) -> tuple:
    """Load a saved FAISS index and its matching chunks."""

    storage_path = Path(storage_dir)
    index_path = storage_path / "index.faiss"
    chunks_path = storage_path / "chunks.json"

    # Make sure both required files exist.
    if not index_path.is_file() or not chunks_path.is_file():
        raise FileNotFoundError(
            "Saved search data is incomplete or does not exist"
        )

    # Restore the saved index and chunk metadata.
    index = faiss.read_index(str(index_path))

    with chunks_path.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    # Check that the saved index and chunks still correspond.
    if not isinstance(chunks, list):
        raise ValueError("Saved chunks must be a list")

    if index.ntotal != len(chunks):
        raise ValueError(
            "Saved index and chunk count do not match. "
            "Rebuild the index before searching."
        )

    return index, chunks
