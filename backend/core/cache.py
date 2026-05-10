import hashlib
import time
from typing import Optional

class QueryCache:
    """
    TTL-based cache for question → answer mappings.
    Avoids re-calling GPT for identical questions.
    """

    def __init__(self, ttl_seconds: int = 3600):
       """
        Args:
            ttl_seconds: How long cached answers remain valid (default: 1 hour)
       """  
       self._cache = {}
       self._ttl = ttl_seconds

    @staticmethod
    def _hash(query: str) -> str:
        normalized = query.strip().lower()
        return hashlib.sha256(normalized.encode()).hexdigest()

    def get(self, query: str) -> Optional[dict]:
        key = self._hash(query)
        entry = self._cache.get(key)
        if entry is None:
            return None

        # Check TTL expiration
        if time.time() - entry["timestamp"] > self._ttl:
            del self._cache[key]
            return None
        return entry["result"]

    def put(self, query: str, result: dict):
        key = self._hash(query)
        self._cache[key] = {
            "result": result,
            "timestamp": time.time()
        }
    def invalidate(self):
        """Clear entire cache (e.g., when a new document is uploaded)."""
        self._cache.clear()


query_cache = QueryCache(ttl_seconds=3600)