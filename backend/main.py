# main.py — FastAPI server, entry point for all agent calls
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Support running from either `backend/` or repository root.
try:
    from graph.workflow import run_workflow  # LangGraph orchestrator (Phase 3)
except ModuleNotFoundError:
    from backend.graph.workflow import run_workflow

app = FastAPI(title="Shopping Assistant API")

# Allow Next.js frontend to call this API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(payload: dict):
    """
    Main endpoint. Receives user query, runs it through LangGraph,
    returns structured product results.
    """
    user_query = payload.get("query", "")
    result = await run_workflow(user_query)
    return result

@app.get("/health")
def health():
    return {"status": "ok"}