from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import requests, os

from app.db.db_base import get_db
from app.db.models import ChatHistory

router = APIRouter(prefix="/chat", tags=["Chat"])

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")
DEFAULT_CITY = "Delhi"

class ChatRequest(BaseModel):
    message: str


def get_weather(city: str = DEFAULT_CITY) -> str:
    try:
        res = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
        if "Unknown location" in res.text or res.status_code != 200:
            return f" Unable to fetch weather for '{city}'"
        return res.text.strip()
    except Exception:
        return " Weather service is currently unavailable."

def fetch_google_results(query: str) -> str:
    try:
        res = requests.get("https://serpapi.com/search", params={
            "q": query,
            "api_key": SERP_API_KEY,
        }, timeout=7)
        data = res.json()
        return data.get("organic_results", [{}])[0].get("snippet", "No relevant results.")
    except Exception as e:
        print("SerpAPI error:", e)
        return " Google search failed."

def query_groq(prompt: str) -> str:
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body, timeout=10)
        data = res.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "⚠️ Groq returned no response.")
    except Exception as e:
        print(" Groq error:", e)
        return " AI failed to respond."

@router.post("/chat")
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    user_message = request.message.strip()
    if not user_message:
        return {"response": " Message is empty."}

    weather = get_weather()
    google = fetch_google_results(user_message)

    prompt = f"""User asked: {user_message}

Google Info:
{google}

Weather in {DEFAULT_CITY}:
{weather}

Now respond helpfully:"""

    reply = query_groq(prompt)

    chat_record = ChatHistory(
        user_id="guest",  
        user_message=user_message,
        bot_response=reply
    )
    db.add(chat_record)
    db.commit()

    return {"response": reply}
