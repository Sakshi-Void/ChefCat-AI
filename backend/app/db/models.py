from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.db.db_base import Base  

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True) 
    user_message = Column(String)
    bot_response = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
