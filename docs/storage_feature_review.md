# ResearchPilot — Storage Feature Preparation

Generated: 2026-10-13 00:18:18

## src\researchpilot\paper_search.py

```python

"""Search research papers using their meaning rather than exact keywords."""

# Import the function that extracts PDF text and splits it into chunks.
from researchpilot.pipeline import process_pdf

# Import the functions that create a searchable vector index
# and use it to find chunks similar in meaning to our question.
from researchpilot.vector_store import build_vector_index, search_vector_index


def search_pdf(
    pdf_path: str,       # The location of the PDF file on the computer.
    query: str,          # The question we want to search for.
    chunk_size: int = 500,  # The maximum target size of each text chunk.
    top_k: int = 3,      # The maximum number of results to return.
) -> list[dict]:         # The function returns a list of result dictionaries.
    """Search a PDF and return its most relevant passages."""

    # Check that we are asking for at least one search result.
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    # If the question is empty or contains only whitespace, stop here.
    # This avoids processing the PDF when there is nothing to search for.
    if not query.strip():
        return []

    # Open the PDF, extract its text, and split that text into chunks.
    # Each chunk also remembers which page it came from.
    chunks = process_pdf(pdf_path, chunk_size=chunk_size)

    # If no text chunks were produced, there is nothing to search.
    if not chunks:
        return []

    # Turn the text chunks into numerical representations called embeddings
    # and store them in a FAISS index so they can be searched.
    index = build_vector_index(chunks)

    # Turn the question into an embedding and search the index for
    # the most similar chunks.
    # We pass the original chunks as well so their text and page numbers
    # can be included in the results.
    results = search_vector_index(
        query=query,
        chunks=chunks,
        index=index,
        top_k=top_k,
    )

    # Give the matching passages back to whoever called this function.
    return results
```

## src\researchpilot\vector_store.py

```python

"""Store text embeddings and search for similar passages using FAISS."""

# FAISS helps us quickly search through numerical representations of text.
import faiss

# NumPy helps us work with arrays of numbers in the format FAISS expects.
import numpy as np

# Reuse the same function that loads the AI embedding model.
from researchpilot.semantic_search import get_embedding_model


def build_vector_index(chunks: list[dict]):
    """Turn text chunks into embeddings and store them in a searchable index."""

    # We cannot build an index if there are no text chunks.
    if not chunks:
        raise ValueError("Cannot build an index with no chunks")

    # Get the AI model, loading it if it has not already been loaded.
    model = get_embedding_model()

    # Collect the text from each chunk into a list.
    # Page numbers and other chunk information are kept in the original chunks.
    texts = [chunk["text"] for chunk in chunks]

    # Convert each text into a list of numbers called an embedding.
    # convert_to_numpy=True returns the embeddings as a NumPy array.
    # normalize_embeddings=True adjusts each vector to have length 1,
    # which makes inner-product scores comparable to cosine similarity.
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    # Make sure the embeddings use float32 numbers, which FAISS expects.
    embeddings = np.asarray(embeddings, dtype="float32")

    # Create a FAISS index that compares vectors using their inner product.
    # embeddings.shape[1] is the number of numbers in each embedding.
    # For this model, each embedding normally contains 384 numbers.
    index = faiss.IndexFlatIP(embeddings.shape[1])

    # Add every chunk's embedding to the index, in the same order as texts.
    index.add(embeddings)

    # Return the completed index so another function can search it.
    return index


def search_vector_index(
    query: str,          # The question we want to search for.
    chunks: list[dict],  # Original chunks containing text and page numbers.
    index,               # The FAISS index built from these chunks.
    top_k: int = 3,       # The maximum number of results to return.
) -> list[dict]:
    """Find the chunks most similar in meaning to the question."""

    # Make sure the requested number of results is at least one.
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    # If the question is blank or there are no chunks, return no results.
    if not query.strip() or not chunks:
        return []

    # Get the same AI embedding model used to create the index.
    model = get_embedding_model()

    # Convert the question into an embedding.
    # [query] puts the question inside a list because the model accepts batches.
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    # Ensure the question embedding uses the float32 format FAISS expects.
    query_embedding = np.asarray(query_embedding, dtype="float32")

    # Search the index for the closest vectors.
    # Search no more than top_k results or the number of available chunks.
    # scores contains similarity scores; indices contains matching positions.
    scores, indices = index.search(
        query_embedding,
        min(top_k, len(chunks)),
    )

    # Create an empty list to collect the matching chunks.
    results = []

    # Examine each returned score alongside its matching index position.
    # scores[0] and indices[0] refer to our single question.
    for score, index_position in zip(scores[0], indices[0]):

        # FAISS uses -1 when a result position is invalid.
        # Skip that entry rather than trying to access a chunk with it.
        if index_position < 0:
            continue

        # Use the returned position to find the original chunk.
        # Copy it so adding a score does not change the original dictionary.
        result = chunks[int(index_position)].copy()

        # Add the similarity score to the result.
        result["score"] = float(score)

        # Save this matching chunk in the results list.
        results.append(result)

    # Return the matching chunks and their scores.
    return results
```

## src\researchpilot\pipeline.py

```python
"""Combine PDF extraction and text chunking."""

from researchpilot.pdf_processing import extract_text_from_pdf
from researchpilot.text_processing import split_into_chunks


def process_pdf(pdf_path: str, chunk_size: int = 500) -> list[dict]:
    """Extract a PDF's text and split it into page-linked chunks."""
    pages = extract_text_from_pdf(pdf_path)
    all_chunks = []

    for page in pages:
        chunks = split_into_chunks(page["text"], chunk_size)

        for chunk in chunks:
            all_chunks.append({
                "page_number": page["page_number"],
                "text": chunk,
            })

    return all_chunks
```

## tests\test_paper_search.py

```python
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
```

## tests\test_vector_store.py

```python
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
```

