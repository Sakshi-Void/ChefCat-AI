from fastapi import APIRouter
from pydantic import BaseModel
import os
import requests

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

def get_weather(city: str = "Delhi") -> str:
    try:
        res = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
        if "Unknown location" in res.text or res.status_code != 200:
            return f"Unable to fetch weather for {city}"
        return res.text.strip()
    except Exception:
        return " Weather service is currently unavailable."

def fetch_google_results(query: str) -> str:
    try:
        params = {
            "q": query,
            "api_key": SERP_API_KEY,
        }
        res = requests.get("https://serpapi.com/search", params=params, timeout=7)
        data = res.json()
        snippet = data.get("organic_results", [{}])[0].get("snippet")
        return snippet or ""
    except Exception as e:
        print(" Google Search failed:", e)
        return ""

def query_groq(prompt: str) -> str:
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": os.getenv("GROQ_MODEL", "llama3-8b-8192"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        res = requests.post(url, headers=headers, json=body, timeout=10)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Groq API error:", e)
        return " AI model failed to respond."

@router.post("/")
def chat_endpoint(request: ChatRequest):
    user_message = request.message


    weather_info = get_weather("Delhi")
    google_info = fetch_google_results(user_message)

    prompt_parts = [f"User asked: {user_message}"]

    if google_info:
        prompt_parts.append(f"\nRelevant Google Info:\n{google_info}")
    if weather_info:
        prompt_parts.append(f"\nCurrent Weather in Delhi:\n{weather_info}")

    prompt_parts.append("\nNow answer concisely and helpfully:")
    prompt = "\n".join(prompt_parts)

    ai_response = query_groq(prompt)

    return {"response": ai_response}
