def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """ 
    Split text into overlapping chunks of fixed-size chunks.

    Args:
        text: Raw document text
        chunk_size: Number of characters per chunk
        overlap:    Number of characters to share between consecutive chunks
    
    Returns:
        List of text chunk strings
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap
        
    return [c for c in chunks if c]