"""Simple keyword-based search for ResearchPilot."""

import re


def search_chunks(
    query: str,
    chunks: list[dict],
    top_k: int = 3,
) -> list[dict]:
    """Return chunks ranked by how many query words they contain."""
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    query_words = set(re.findall(r"\w+", query.lower()))

    if not query_words:
        return []

    results = []

    for chunk in chunks:
        text_words = set(re.findall(r"\w+", chunk["text"].lower()))
        score = len(query_words & text_words)

        if score > 0:
            results.append({**chunk, "score": score})

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:top_k]
