
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
