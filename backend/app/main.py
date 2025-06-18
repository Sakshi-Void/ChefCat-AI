
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.db_base import Base, engine


from app.api import chat, history
from app.routes import documents

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ChefCat.AI Backend",
    description="AI assistant with chat, documents, and weather support",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"  ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(history.router, prefix="/api/history", tags=["History"])
for route in app.routes:
    print(f"✅ ROUTE: {route.path} → {route.name}")


@app.get("/")
def root():
    return {"message": "✅ ChefCat.AI backend is running"}
    
