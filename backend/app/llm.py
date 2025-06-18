import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_response(message: str) -> str:
    if not GROQ_API_KEY:
        return " Missing GROQ_API_KEY in environment."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "user", "content": message}
            ],
            "temperature": 0.7
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=10)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print(" Groq API Error:", response.status_code, response.text)
            return " Error generating response from Groq."

    except Exception as e:
        print(" Exception in generate_response:", str(e))
        return " Internal server error"
