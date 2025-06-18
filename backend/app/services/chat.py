from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.services.chat import get_llm_answer
from app.db.db_base import get_db
from app.db.models import ChatHistory

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@router.post("/talk")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    prompt = req.message

    response = get_llm_answer(prompt)

    chat_entry = ChatHistory(
        user_id=req.user_id,
        user_message=prompt,
        bot_response=response,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)

    return {"response": response}
