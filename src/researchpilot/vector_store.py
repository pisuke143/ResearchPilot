"""Vector storage and similarity search for ResearchPilot."""

import faiss
import numpy as np

from researchpilot.semantic_search import get_embedding_model


def build_vector_index(chunks: list[dict]):
    """Build a FAISS index from text chunks."""
    if not chunks:
        raise ValueError("Cannot build an index with no chunks")

    model = get_embedding_model()
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index


def search_vector_index(
    query: str,
    chunks: list[dict],
    index,
    top_k: int = 3,
) -> list[dict]:
    """Find the most similar chunks using a FAISS index."""
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    if not query.strip() or not chunks:
        return []

    model = get_embedding_model()

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    query_embedding = np.asarray(query_embedding, dtype="float32")

    scores, indices = index.search(
        query_embedding,
        min(top_k, len(chunks)),
    )

    results = []

    for score, index_position in zip(scores[0], indices[0]):
        if index_position < 0:
            continue

        result = chunks[int(index_position)].copy()
        result["score"] = float(score)
        results.append(result)

    return results
