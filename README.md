# Multi-Agent Shopping Assistant

A LangGraph-powered shopping assistant with specialized AI agents.

## Tech Stack
- **Backend**: Python, FastAPI, LangGraph, LangChain, SQLite
- **Frontend**: Next.js (TypeScript)
- **LLM**: GPT-4o-mini via OpenRouter/OpenAI

## Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install && npm run dev
```

## Architecture
- Router Agent → classifies intent
- Search Agent → SerpAPI Google Shopping
- Recommendation Agent → LLM ranking
- Comparison Agent → LLM table generation
- Budget Agent → price filtering
- Formatter → structured JSON response