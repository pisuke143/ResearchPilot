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
