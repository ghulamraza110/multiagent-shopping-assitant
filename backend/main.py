# main.py — FastAPI server. Updated to handle the new workflow response shape.

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
import os

# Load environment variables from .env file
load_dotenv()

# Import workflow AFTER load_dotenv so env vars are available
from graph.workflow import run_workflow

# Initialize FastAPI app with metadata
app = FastAPI(title="Shopping Assistant API", version="2.0.0")

# Enable CORS for frontend (Next.js running on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Only allow frontend origin
    allow_methods=["*"],                      # Allow all HTTP methods
    allow_headers=["*"],                      # Allow all headers
)

# Define request body schema using Pydantic
class ChatRequest(BaseModel):
    """Typed request body — better than a raw dict."""
    query: str  # User query string


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Shopping Assistant API is running"}


# Chat endpoint — main entry point for queries
@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Receives user query, runs it through the single-agent LangGraph workflow,
    returns structured response with products, answer, and comparison table.
    """
    # Validate query is not empty
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        # Run workflow with user query and return structured result
        result = await run_workflow(request.query)
        return result
    except Exception as e:
        # Catch errors and return as HTTP 500
        raise HTTPException(status_code=500, detail=str(e))
