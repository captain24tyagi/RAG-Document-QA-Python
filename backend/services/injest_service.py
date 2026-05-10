from core.chunker import chunk_text
from core.embedder import embed_texts
from core.vector_store import VectorStore
from core.cache import query_cache


store = VectorStore(dimension=1536)

def ingest_document(text: str) -> dict:

    # Step 1: Split document into chunks
    chunks = chunk_text(text, chunk_size=500, overlap=50)

    if not chunks:
        raise ValueError("Document produced no chunks after splitting.")

    embeddings = embed_texts(chunks)

    store.add(chunks, embeddings)

    # Invalidate Q&A cache — answers may change with new document

    query_cache.invalidate()

    return {
        "chunks_stored": store.total_chunks,
        "new_chunks": len(chunks)
    }
