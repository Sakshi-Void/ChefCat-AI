from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.api import chat, history
from app.routes import documents
from app.db.db_base import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ChefCat.AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(chat.router, prefix="/api/chat")
app.include_router(documents.router, prefix="/api/documents")
app.include_router(history.router, prefix="/api/history")

@app.get("/")
def root():
    return {"message": "ChefCat.AI backend running"}

# Required for Vercel serverless
handler = Mangum(app)
