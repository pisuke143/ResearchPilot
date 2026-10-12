
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
