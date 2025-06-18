from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from PyPDF2 import PdfReader

from app.qdrant_utils import upload_chunks, search_similar_chunks, clear_qdrant 
from app.llm import generate_response

router = APIRouter()

def split_pdf_into_chunks(file: UploadFile, chunk_size: int = 500) -> list:
    reader = PdfReader(file.file)
    full_text = " ".join(page.extract_text() or "" for page in reader.pages)
    words = full_text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        clear_qdrant()  
        chunks = split_pdf_into_chunks(file)
        upload_chunks(chunks)
        return {"message": f"Uploaded {len(chunks)} chunks to Qdrant"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask-pdf/")
async def ask_pdf(req: QuestionRequest):
    try:
        question = req.question
        top_chunks = search_similar_chunks(question, k=5)
        context = "\n".join(top_chunks)

        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        answer = generate_response(prompt)

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ask failed: {str(e)}")
