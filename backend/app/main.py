from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# import routes
from app.api import chat, history
from app.routes import documents
from app.db.db_base import Base, engine

# Database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(title="ChefCat.AI Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routes
app.include_router(chat.router, prefix="/api/chat")
app.include_router(documents.router, prefix="/api/documents")
app.include_router(history.router, prefix="/api/history")

@app.get("/")
def root():
    return {"message": "ChefCat.AI backend running"}

# Mangum handler
handler = Mangum(app)
