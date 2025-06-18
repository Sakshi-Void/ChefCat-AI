from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timezone

from app.db.db_base import get_db
from app.db.models import ChatHistory

router = APIRouter(tags=["History"])

class HistoryCreate(BaseModel):
    user_id: str
    user_message: str
    bot_response: str

@router.post("/save")
def save_message(payload: HistoryCreate, db: Session = Depends(get_db)):
    chat = ChatHistory(
        user_id=payload.user_id,
        user_message=payload.user_message,
        bot_response=payload.bot_response,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return {"message": "Saved", "id": chat.id}

@router.get("/all/{user_id}")
def get_all_history(user_id: str, db: Session = Depends(get_db)):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.timestamp.desc())
        .all()
    )

