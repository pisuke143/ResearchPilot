
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
