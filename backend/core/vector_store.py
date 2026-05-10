import numpy as np
import faiss

class VectorStore:
    """
    In-memory FAISS vector store using cosine similarity (via normalized inner product).
    """

    def __init__(self, dimension: int=1536):

        """
        Initialize a FAISS flat inner-product index.
        
        Args:
            dimension: Size of each embedding vector (1536 for text-embedding-3-small)
        """

        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks: list[str] = []

    def add(self, chunks: list[str], embeddings: list[list[float]]):

        """
        Add text chunks and their embeddings to the store.
        
        Args:
            chunks:     List of raw text strings
            embeddings: Corresponding embedding vectors
        """
        
        vectors = np.array(embeddings, dtype=np.float32)
        faiss.normalize_L2(vectors)
        self.index.add(vectors)

        self.chunks.extend(chunks)

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[str]:

        """
        Find the top-k most similar chunks for a query embedding.
        
        Args:
            query_embedding: The query vector to search against
            top_k:           Number of results to return
        
        Returns:
            List of dicts: [{ "text": str, "score": float }, ...]
            Ordered by descending cosine similarity score.
        """

        query_vec = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_vec)  # normalize query too

        # D = distances (cosine scores here), I = indices
        D, I = self.index.search(query_vec, top_k)

        results = []
        for score, idx in zip(D[0], I[0]):
            if idx == -1:
                continue
            results.append({
                "text": self.chunks[idx],
                "score": float(score)
            })
        
        return results

    def reset(self):
        self.index = faiss.IndexFlatIP(self.dimension)
        self.chunks = []

    @property
    def total_chunks(self) -> int:
        return self.index.ntotal