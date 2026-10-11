"""Meaning-based search for ResearchPilot."""

from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None


def get_embedding_model():
    """Load the model once and reuse it."""
    global _model

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def semantic_search(
    query: str,
    chunks: list[dict],
    top_k: int = 3,
) -> list[dict]:
    """Find chunks whose meanings are closest to the question."""
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    if not query.strip() or not chunks:
        return []

    model = get_embedding_model()

    chunk_texts = [chunk["text"] for chunk in chunks]

    query_embedding = model.encode(
        query,
        convert_to_tensor=True,
    )

    chunk_embeddings = model.encode(
        chunk_texts,
        convert_to_tensor=True,
    )

    scores = util.cos_sim(query_embedding, chunk_embeddings)[0]

    ranked_indices = scores.argsort(descending=True)[:top_k]

    results = []

    for index in ranked_indices:
        result = chunks[int(index)].copy()
        result["score"] = float(scores[index])
        results.append(result)

    return results
