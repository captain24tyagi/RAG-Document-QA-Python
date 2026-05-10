from core.embedder import embed_query
from core.vector_store import VectorStore

MIN_SCORE_THRESHOLD = 0.3

def retrieve(query: str, store: VectorStore, top_k: int = 5):

    """
    Retrieve the top-k most relevant chunks for a user query.
    
    Flow:
        1. Embed the query string into a vector
        2. Search the FAISS index for the nearest vectors
        3. Return the corresponding text chunks with their similarity scores
    
    Args:
        query:  The user's question string
        store:  The VectorStore instance holding document embeddings
        top_k:  Number of chunks to return
    
    Returns:
        List of { "text": str, "score": float } dicts, best match first
    """

    query_vector = embed_query(query)
    results = store.search(query_vector, top_k=top_k)

    filtered = [r for r in results if r["score"] >= MIN_SCORE_THRESHOLD]

    print('res_retrieve: ', filtered)

    return filtered




