# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from mangum import Mangum


# from app.api import chat, history
# from app.routes import documents
# from app.db.db_base import Base, engine

# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="ChefCat.AI Backend")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], 
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# app.include_router(chat.router, prefix="/api/chat")
# app.include_router(documents.router, prefix="/api/documents")
# app.include_router(history.router, prefix="/api/history")

# @app.get("/")
# def root():
#     return {"message": "ChefCat.AI backend running"}

# handler = Mangum(app)

# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

# --- your project imports ---
from app.api import chat, history
from app.routes import documents
from app.db.db_base import Base, engine

# Create tables (idempotent; okay for serverless cold start)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ChefCat.AI Backend")

# --- CORS (add your Vercel domain below) ---
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    os.getenv("FRONTEND_ORIGIN", "https://<YOUR-PROJECT>.vercel.app"),
    "*"  # if you want to keep it wide open; for production, prefer exact domains
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers (already mounted under /api/...) ---
app.include_router(chat.router,      prefix="/api/chat")
app.include_router(documents.router, prefix="/api/documents")
app.include_router(history.router,   prefix="/api/history")

@app.get("/")
def root():
    return {"message": "ChefCat.AI backend running"}

# --- Optional health check to verify Groq + Qdrant on Vercel ---
@app.get("/api/health")
def health():
    out = {"groq": {}, "qdrant": {}}

    # Groq check
    try:
        gkey = os.getenv("GROQ_API_KEY")
        if gkey:
            r = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {gkey}"},
                timeout=8,
            )
            out["groq"] = {"ok": r.ok, "status": r.status_code}
        else:
            out["groq"] = {"ok": False, "error": "GROQ_API_KEY not set"}
    except Exception as e:
        out["groq"] = {"ok": False, "error": str(e)}

    # Qdrant check
    try:
        qurl = os.getenv("QDRANT_URL")
        qkey = os.getenv("QDRANT_API_KEY")
        qcol = os.getenv("QDRANT_COLLECTION_NAME", "chefcat")
        if qurl:
            hz = requests.get(f"{qurl}/healthz", timeout=5)
            out["qdrant"]["healthz"] = hz.ok
            if qkey:
                col = requests.get(
                    f"{qurl}/collections/{qcol}",
                    headers={"Authorization": f"apikey {qkey}"},
                    timeout=8,
                )
                out["qdrant"]["collection_ok"] = col.ok
                out["qdrant"]["collection_status"] = col.status_code
            else:
                out["qdrant"]["error"] = "QDRANT_API_KEY not set"
        else:
            out["qdrant"] = {"ok": False, "error": "QDRANT_URL not set"}
    except Exception as e:
        out["qdrant"] = {"ok": False, "error": str(e)}

    ok = bool(out.get("groq", {}).get("ok")) and bool(out.get("qdrant", {}).get("healthz"))
    return {"ok": ok, **out}

# --- Optional: keep Mangum for AWS, Vercel ignores it but won't break ---
try:
    from mangum import Mangum
    handler = Mangum(app)
except Exception:
    handler = None
