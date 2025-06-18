import os
import requests
from app.utils.pdf_utils import extract_text_from_pdf, chunk_text
from backend.app.qdrant_utils import create_collection, add_chunks_to_qdrant, search_chunks
from app.config import settings  

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


create_collection()


def handle_pdf_upload(file) -> str:
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    add_chunks_to_qdrant(chunks)

    return " PDF processed and stored."


def answer_question_from_pdf(query: str) -> str:
    context_chunks = search_chunks(query)
    context = "\n".join(context_chunks) or "No relevant context found."

    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Answer using this context:\n{context}\n\nQ: {query}"}
        ]
    }

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", " No content returned.")
    except requests.exceptions.RequestException as e:
        print("Groq request error:", e)
        return " Failed to get an answer from the AI."
    except Exception as e:
        print("Unexpected error:", e)
        return " Internal error while answering your question."
