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

def upsert_texts(texts: list[str], embeddings: list[list[float]], source: str) -> int:
    ensure_collection(len(embeddings[0]))
    points = []
    for text, vector in zip(texts, embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": text, "source": source},
            )
        )
    client.upsert(collection_name=settings.qdrant_collection, points=points)
    return len(points)

def search(query_vector: list[float], top_k: int = 4) -> list[str]:
    hits = client.search(
        collection_name=settings.qdrant_collection,
        query_vector=query_vector,
        limit=top_k,
    )
    return [h.payload.get("text", "") for h in hits]
