"""Search research papers using their meaning rather than exact keywords."""

# process_pdf extracts PDF text and splits it into page-linked chunks.
from researchpilot.pipeline import process_pdf

# These functions build an index and search it using text embeddings.
from researchpilot.vector_store import build_vector_index, search_vector_index


def search_pdf(
    pdf_path: str,
    query: str,
    chunk_size: int = 500,
    top_k: int = 3,
) -> list[dict]:
    """Search a PDF and return its most relevant passages."""

    # Step 1: Validate top_k before doing expensive PDF or model work.
    # top_k is the maximum number of search results to return.
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    # Step 2: If the question is blank, there is nothing to search for.
    # Return early without opening the PDF or loading the AI model.
    if not query.strip():
        return []

    # Step 3: Extract the PDF's text and split it into manageable chunks.
    # Each chunk includes its text and the page number it came from.
    chunks = process_pdf(pdf_path, chunk_size=chunk_size)

    # Step 4: Handle PDFs that contain no extractable text.
    # We cannot build a useful index if there are no chunks.
    if not chunks:
        return []

    # Step 5: Convert the chunks into embeddings and build a FAISS index.
    # The index helps us find passages whose meanings match the question.
    index = build_vector_index(chunks)

    # Step 6: Search the index using the user's question.
    # The original chunks are passed too, so results retain page numbers.
    results = search_vector_index(
        query=query,
        chunks=chunks,
        index=index,
        top_k=top_k,
    )

    # Step 7: Return the best-matching passages to the caller.
    return results
