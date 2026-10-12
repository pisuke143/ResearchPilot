
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
