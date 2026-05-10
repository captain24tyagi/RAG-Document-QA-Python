import os
from openai import OpenAI
from dotenv import load_dotenv
from core.embedding_cache import embedding_cache

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embed a list of text strings using OpenAI text-embedding-3-small.
    
    Args:
        texts: List of strings to embed
    
    Returns:
        List of embedding vectors (each is a list of 1536 floats)
    """
    
    results = [None] * len(texts)
    uncached_indices = []
    uncached_texts = []

    for i, text in enumerate(texts):
        cached = embedding_cache.get(text)
        if cached is not None:
            results[i] = cached
            print('cached: ', results[i])
        else:
            uncached_indices.append(i)
            uncached_texts.append(text)

    if uncached_texts:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=uncached_texts
        )

        new_embeddings = [item.embedding for item in response.data]
        #print('embeddings: ', [item.embedding for item in response.data])

        for idx, embedding in zip(uncached_indices, new_embeddings):
            results[idx] = embedding

        embedding_cache.put_batch(uncached_texts, new_embeddings)

    #print('embeddings_final: ', results)

    return results

    # response = client.embeddings.create(
    #     model="text-embedding-3-small",
    #     input=texts
    # )

    # print('embeddings: ', [item.embedding for item in response.data])

    # return [item.embedding for item in response.data]


def embed_query(query: str) -> list[float]:
    """
    Embed a single query string.
    
    Args:
        query: The user's question
    
    Returns:
        A single embedding vector (list of 1536 floats)
    """

    return embed_texts([query])[0]