# from dotenv import load_dotenv
# load_dotenv()

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.db.db_base import Base, engine
# from mangum import Mangum

# from app.api import chat, history
# from app.routes import documents

# # Create database tables
# Base.metadata.create_all(bind=engine)

# # Initialize FastAPI app
# app = FastAPI(
#     title="ChefCat.AI Backend",
#     description="AI assistant with chat, documents, and weather support",
#     version="1.0.0"
# )

# # CORS Middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include Routers
# app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
# app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
# app.include_router(history.router, prefix="/api/history", tags=["History"])

# # Debug: Print all routes
# for route in app.routes:
#     print(f"✅ ROUTE: {route.path} → {route.name}")

# # Root endpoint
# @app.get("/")
# def root():
#     return {"message": "✅ ChefCat.AI backend is running"}

# # Vercel serverless handler
# handler = Mangum(app)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# Import your routes and database
from app.db.db_base import Base, engine
from app.api import chat, history
from app.routes import documents

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ChefCat.AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat")
app.include_router(documents.router, prefix="/api/documents")
app.include_router(history.router, prefix="/api/history")

@app.get("/")
def root():
    return {"message": "ChefCat.AI backend running"}

handler = Mangum(app)  # Required for serverless
