import hashlib
from typing import Optional

class EmbeddingCache:

    """
    In-memory cache: text_hash → embedding vector.
    Avoids re-calling OpenAI for identical text chunks.
    """

    def __init__(self):
        self._cache: dict[str, list[float]] = {}
        self._hits = 0
        self._misses = 0

    @staticmethod
    def _hash(text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    def get(self, text: str) -> Optional[list[float]]:
        key = self._hash(text)
        if key in self._cache:
            self._hits += 1
            return self._cache[key]
        self._misses += 1
        return None
    
    def put(self, text: str, embedding: list[float]):
        key = self._hash(text)
        self._cache[key] = embedding

    def put_batch(self, texts: list[str], embeddings: list[list[float]]):
        for text, emb in zip(texts, embeddings):
            self.put(text, emb)

    @property
    def stats(self) -> dict:
        total = self._hits + self._misses
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{(self._hits / total * 100):.1f}%" if total > 0 else "0%",
            "cached_items": len(self._cache)
        }

embedding_cache = EmbeddingCache()
