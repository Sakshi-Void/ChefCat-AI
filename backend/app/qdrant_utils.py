from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, ScoredPoint
from sentence_transformers import SentenceTransformer
from uuid import uuid4
from typing import List, Optional

model = SentenceTransformer("all-MiniLM-L6-v2")

qdrant_client = QdrantClient(
    url="https://55f34e69-d2c2-408d-aa15-3b0e1d64b7df.us-east4-0.gcp.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0._OOSTU5rMB-eSqYGKCq7zRNCjtSDvzwEEZ1Xmch9XvQ",
)

COLLECTION_NAME = "pdf_chunks"


def create_collection_if_not_exists(vector_size: int):
    collections = qdrant_client.get_collections().collections
    if not any(col.name == COLLECTION_NAME for col in collections):
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


def clear_qdrant():
    try:
        if qdrant_client.collection_exists(COLLECTION_NAME):
            qdrant_client.delete_collection(collection_name=COLLECTION_NAME)
            print("✅ Previous Qdrant collection deleted.")
    except Exception as e:
        print(f"❌ Failed to clear Qdrant collection: {e}")


def upload_chunks(chunks: List[str], metadata: Optional[List[dict]] = None):
    vectors = model.encode(chunks).tolist()
    create_collection_if_not_exists(len(vectors[0]))

    points = []
    for idx, vector in enumerate(vectors):
        payload = metadata[idx] if metadata else {"chunk": chunks[idx]}
        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=vector,
                payload=payload
            )
        )

    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)


def search_similar_chunks(query: str, k: int = 5) -> List[str]:
    vector = model.encode(query).tolist()
    results: List[ScoredPoint] = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=k,
    )
    return [hit.payload.get("chunk", "") for hit in results]
