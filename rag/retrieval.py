from apps.api.ollama_client import embed, rerank
from rag.qdrant_store import search

async def retrieve_contexts(question: str, top_k: int) -> list[dict]:
    query_vector = (await embed([question]))[0]
    results = search(query_vector, top_k=top_k)
    texts = [r["text"] for r in results]
    reranked = await rerank(question, texts)
    if reranked == texts:
        return results
    # basic mapping back by text identity
    order = {text: i for i, text in enumerate(reranked)}
    return sorted(results, key=lambda r: order.get(r["text"], 999999))
