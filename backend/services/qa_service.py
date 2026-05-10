import os
from openai import OpenAI
from core.retriever import retrieve
from services.injest_service import store
from core.cache import query_cache

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def answer_question(query: str, top_k: int = 5) -> dict:

    if store.total_chunks == 0:
        return {
            "answer": "No documents have been uploaded yet. Please upload a document first.",
            "source_chunks": []
        }

    cached = query_cache.get(query)
    if cached:
        return cached


    retrieved = retrieve(query, store, top_k=top_k)
    print('retrieved: ', retrieved)
        

    context = "\n\n---\n\n".join([r["text"] for r in retrieved])

    system_prompt = (
        "You are a helpful assistant. Answer the user's question based ONLY on the "
        "provided context. If the answer is not found in the context, say "
        "'I don't have enough information in the uploaded document to answer that.'"
        "\n\nDo not make up information. Be concise and accurate."
    )

    user_prompt = f"Context:\n{context}\n\nQuestion: {query}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=5000
    )

    answer = response.choices[0].message.content

    result = {
        "answer": answer,
        "source_chunks": retrieved
    }

    # Cache for future identical queries
    query_cache.put(query, result)

    return result

        
