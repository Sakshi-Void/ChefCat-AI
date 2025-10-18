import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, ScoredPoint
from sentence_transformers import SentenceTransformer
from uuid import uuid4
from typing import List, Optional
from dotenv import load_dotenv
load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "pdf_chunks")

model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    prefer_grpc=False,
    check_compatibility=False  
)

def create_collection_if_not_exists(vector_size: int):
    try:
        collections = [col.name for col in qdrant_client.get_collections().collections]
        if COLLECTION_NAME not in collections:
            qdrant_client.recreate_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            print(f"Qdrant collection '{COLLECTION_NAME}' created.")
    except Exception as e:
        print(f"Failed to create collection: {e}")

def clear_qdrant():
    try:
        collections = [col.name for col in qdrant_client.get_collections().collections]
        if COLLECTION_NAME in collections:
            qdrant_client.delete_collection(collection_name=COLLECTION_NAME)
            print(f"Qdrant collection '{COLLECTION_NAME}' deleted.")
    except Exception as e:
        print(f"Failed to clear Qdrant collection: {e}")

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

    try:
        qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f" {len(points)} chunks uploaded to '{COLLECTION_NAME}'.")
    except Exception as e:
        print(f"Failed to upload chunks: {e}")

def search_similar_chunks(query: str, k: int = 5) -> List[str]:
    vector = model.encode(query).tolist()
    try:
        results: List[ScoredPoint] = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=k
        )
        return [hit.payload.get("chunk", "") for hit in results]
    except Exception as e:
        print(f"Qdrant search failed: {e}")
        return []
