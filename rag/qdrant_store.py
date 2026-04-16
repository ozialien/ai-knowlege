from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from apps.api.config import settings
import uuid

client = QdrantClient(url=settings.qdrant_url)

def ensure_collection(vector_size: int) -> None:
    collections = [c.name for c in client.get_collections().collections]
    if settings.qdrant_collection not in collections:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

def upsert_texts(texts: list[str], embeddings: list[list[float]], source: str, payloads: list[dict] | None = None) -> int:
    ensure_collection(len(embeddings[0]))
    payloads = payloads or [{} for _ in texts]
    points = []
    for text, vector, payload in zip(texts, embeddings, payloads):
        merged = {"text": text, "source": source}
        merged.update(payload or {})
        points.append(PointStruct(id=str(uuid.uuid4()), vector=vector, payload=merged))
    client.upsert(collection_name=settings.qdrant_collection, points=points)
    return len(points)

def search(query_vector: list[float], top_k: int = 4) -> list[dict]:
    hits = client.search(
        collection_name=settings.qdrant_collection,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
    )
    return [{
        "text": h.payload.get("text", ""),
        "source": h.payload.get("source", ""),
        "path": h.payload.get("path", ""),
        "title": h.payload.get("title", ""),
        "chunk_index": h.payload.get("chunk_index", -1),
    } for h in hits]
