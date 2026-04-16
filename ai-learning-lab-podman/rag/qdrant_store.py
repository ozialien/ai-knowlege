import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from apps.api.config import settings

client = QdrantClient(url=settings.qdrant_url)

def ensure_collection(vector_size: int):
    collections = [c.name for c in client.get_collections().collections]
    if settings.qdrant_collection not in collections:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

def upsert_records(records: list[dict], vectors: list[list[float]]):
    ensure_collection(len(vectors[0]))
    points = []
    for rec, vec in zip(records, vectors):
        points.append(PointStruct(id=str(uuid.uuid4()), vector=vec, payload=dict(rec)))
    client.upsert(collection_name=settings.qdrant_collection, points=points)
    return len(points)

def search(query_vector: list[float], top_k: int = 5):
    hits = client.search(
        collection_name=settings.qdrant_collection,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
    )
    return [h.payload for h in hits]
