import httpx
from apps.api.config import settings

async def chat(message: str, system: str | None = None) -> str:
    payload = {
        "model": settings.ollama_chat_model,
        "messages": [
            {"role": "system", "content": system or "You are a helpful assistant."},
            {"role": "user", "content": message},
        ],
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(f"{settings.ollama_base_url}/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["message"]["content"]

async def embed(texts: list[str]) -> list[list[float]]:
    results = []
    async with httpx.AsyncClient(timeout=120) as client:
        for text in texts:
            payload = {"model": settings.ollama_embed_model, "prompt": text}
            resp = await client.post(f"{settings.ollama_base_url}/api/embeddings", json=payload)
            resp.raise_for_status()
            results.append(resp.json()["embedding"])
    return results

async def rerank(query: str, documents: list[str]) -> list[str]:
    if not settings.enable_rerank or not settings.ollama_rerank_model or not documents:
        return documents
    return documents
