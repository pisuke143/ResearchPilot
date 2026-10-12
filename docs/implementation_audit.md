# ResearchPilot - Implementation Audit

Generated: 2026-10-13 00:16:33

## Source modules

### paper_search.py

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

### pdf_processing.py

```python
"""Utilities for extracting text from PDF documents."""

from pathlib import Path
import pymupdf


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """Extract text from a PDF, keeping each page's number."""
    pdf_path = Path(pdf_path)
    # check if the PDF file exists at that location before trying to open it
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    # empty list of pages
    pages = []
    # using pymupdf to open the PDF and extract text from each page
    with pymupdf.open(pdf_path) as document:
        # iterate through each page in the PDF, starting with page number 1
        for page_number, page in enumerate(document, start=1):
            # extract the text from the page and append it to the list of pages
            pages.append({
                "page_number": page_number,
                "text": page.get_text(),
            })

    return pages
```

### pipeline.py

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

### retrieval.py

```python

"""Simple keyword-based search for ResearchPilot."""

import re  # Helps us find and extract words from text.


def search_chunks(
    query: str,          # The question or words the user wants to search for.
    chunks: list[dict],  # The text chunks we want to search through.
    top_k: int = 3,      # The maximum number of results to return.
) -> list[dict]:         # The function returns a list of matching chunks.
    """Return chunks ranked by how many query words they contain."""

    # Make sure the user asks for at least one result.
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    # Convert the query to lowercase and extract its words.
    # Using a set removes duplicate words.
    query_words = set(re.findall(r"\w+", query.lower()))

    # If the query contains no words, there is nothing to search for.
    if not query_words:
        return []

    # Create an empty list to store matching chunks and their scores.
    results = []

    # Examine each chunk one by one.
    for chunk in chunks:

        # Convert the chunk's text to lowercase and extract its words.
        # A set keeps each word only once.
        text_words = set(re.findall(r"\w+", chunk["text"].lower()))

        # Count how many distinct query words also appear in this chunk.
        score = len(query_words & text_words)

        # Keep only chunks that match at least one query word.
        if score > 0:
            # Copy the chunk's information and add its matching-word score.
            # The original chunk dictionary is not modified.
            results.append({**chunk, "score": score})

    # Sort results from the highest score to the lowest score.
    results.sort(key=lambda item: item["score"], reverse=True)

    # Return only the first top_k results.
    return results[:top_k]
```

### semantic_search.py

```python

"""Find text chunks that have a meaning similar to a question."""

from sentence_transformers import SentenceTransformer, util

# The name of the AI model ResearchPilot uses to understand text.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# These variables remember things so we don't have to calculate or load them again.
_model = None
_cached_texts = None
_cached_embeddings = None


def get_embedding_model():
    """Load the AI model once and reuse it."""

    # Allow this function to use and update the _model variable above.
    global _model

    # If the model has not been loaded yet, load it now.
    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(MODEL_NAME)

    # Give the loaded model back to the code that requested it.
    return _model


def semantic_search(
    query: str,
    chunks: list[dict],
    top_k: int = 3,
) -> list[dict]:
    """Find the chunks whose meanings are most similar to the question."""

    # Allow this function to update the saved text and embedding information.
    global _cached_texts, _cached_embeddings

    # Make sure the requested number of results is at least one.
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    # If the question is empty or there is no text to search, return no results.
    if not query.strip() or not chunks:
        return []

    # Get the AI model, loading it first if necessary.
    model = get_embedding_model()

    # Collect the text from every chunk into a list.
    chunk_texts = [chunk["text"] for chunk in chunks]

    # Only calculate the chunk embeddings again if the text has changed.
    if chunk_texts != _cached_texts:
        # Turn each chunk into numbers that represent its meaning.
        _cached_embeddings = model.encode(
            chunk_texts,
            convert_to_tensor=True,
        )

        # Remember which texts these embeddings belong to.
        _cached_texts = chunk_texts

    # Turn the user's question into numbers that represent its meaning.
    query_embedding = model.encode(
        query,
        convert_to_tensor=True,
    )

    # Compare the question with every chunk and calculate similarity scores.
    scores = util.cos_sim(query_embedding, _cached_embeddings)[0]

    # Arrange chunk positions from the highest score to the lowest,
    # and keep only the requested number of results.
    ranked_indices = scores.argsort(descending=True)[:top_k]

    # Create an empty list to hold the best matching chunks.
    results = []

    # Go through the positions of the best-matching chunks.
    for index in ranked_indices:
        # Copy the original chunk so we can add a score without changing it.
        result = chunks[int(index)].copy()

        # Save the similarity score alongside the chunk's existing information.
        result["score"] = float(scores[index])

        # Add this chunk and its score to the results list.
        results.append(result)

    # Return the matching chunks, starting with the highest similarity score.
    return results
```

### text_processing.py

```python
"""Basic text-processing utilities for ResearchPilot."""


def split_into_chunks(text: str, chunk_size: int = 200) -> list[str]:
    """Split text into chunks containing at most chunk_size characters."""
    # Reject invalid chunk sizes before processing the text.
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    # Tokenize on whitespace so we preserve words and avoid splitting mid-word.
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        # Check whether adding this word would exceed the configured size limit.
        candidate = " ".join(current_chunk + [word])

        if len(candidate) > chunk_size and current_chunk:
            # Flush the completed chunk and start a fresh one with the current word.
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
        else:
            current_chunk.append(word)

    # Add any remaining words as the final chunk.
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
```

### vector_store.py

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

### __init__.py

```python
"""ResearchPilot: an evidence-grounded research paper assistant."""

__version__ = "0.1.0"
```

## Test modules

- test_paper_search.py
- test_pipeline.py
- test_retrieval.py
- test_semantic_search.py
- test_text_processing.py
- test_vector_store.py

## Current test baseline

Latest manually observed result: 21 tests passed in 5.671 seconds.
Rerun tests before relying on this result after code changes.

## Planned components to verify

- Persistent document storage
- Saved and reloadable vector indexes
- Hybrid retrieval
- Evidence-grounded answer generation
- Citation validation
- User interface
- Multi-paper library workflow
- End-to-end evaluation
