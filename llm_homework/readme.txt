SMART LIBRARIAN - AI BOOK RECOMMENDER

Technologies:
- Backend: FastAPI + OpenAI (GPT, Whisper, DALL·E)
- Frontend: React (Vite)
- Vector Store: ChromaDB
- TTS: gTTS + pygame
- STT: Web Speech API or Whisper API
- Image Generation: DALL·E 2
- Language Filter: Yes

PROJECT STRUCTURE:
- backend/       → FastAPI REST API
- frontend/      → React + Vite web interface
- llm/           → GPT, TTS, STT, tools
- retriever/     → ChromaDB + embeddings
- data/          → book_summaries.txt
- images/, audio/ → generated files

HOW TO RUN:

1. Backend (Python 3.10+)
----------------------------------
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000

2. Frontend
----------------------------------
cd frontend
npm install
npm run dev

3. Access in browser:
----------------------------------
Backend docs:  http://localhost:8000/docs
Frontend app:  http://localhost:5173

ENV VARIABLES:
OPENAI_API_KEY=sk-...

REQUIREMENTS COVERED:
- [x] RAG with GPT
- [x] Tool calling
- [x] Browser UI
- [x] TTS + STT
- [x] AI-generated image
- [x] Offensive language filter
