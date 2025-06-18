# ChefCat.AI

ChefCat.AI is a fullstack AI assistant built as part of an internship project. It offers an intelligent chat interface, weather updates, PDF Q&A, web search, and voice features — all through a sleek, user-friendly UI.

---

## Features

- LLM Chat – Natural conversation powered by Groq (LLaMA3)
- PDF Q&A – Upload any PDF and ask context-aware questions (RAG + Qdrant Cloud)
- Live Weather – Real-time weather via wttr.in
- Web Search – Uses SerpAPI for intelligent fallback answers
- Voice Input + TTS – Speak to the bot and hear it reply using pyttsx3
- Dark/Light Mode – Toggle using TailwindCSS
- Chat History – Restore previous chats
- User Session UX – Smooth experience with persistent tabs

---

## Tech Stack

- **Frontend**: React + TypeScript, TailwindCSS, Axios, React Router DOM, Voice Input UI
- **Backend**: FastAPI (Python), pyttsx3 (TTS), CORS, dotenv config
- **AI + RAG**: Groq (LLaMA3-8B), Qdrant Cloud, SentenceTransformers, RAG pipeline
- **APIs**: wttr.in (weather), SerpAPI (web search)

---

## Project Tabs

- Chat – Main LLM interface  
- Documents – PDF upload, Q&A, and Search  
- History – Previous user conversations  
- Settings – Personalization, dark/light toggle  
- Help – Project guide and assistant usage

---

## Local Setup

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
