"""
Minimal FastAPI app — just enough to prove the backend can talk to
Ollama over HTTP. No agent, no RAG, no LangGraph yet. That's later phases.

Run with:  uvicorn backend.main:app --reload
Then visit http://localhost:8000/docs
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from pydantic import BaseModel

from llm.ollama_client import OllamaClient

app = FastAPI(title="AgentForge", version="0.1.0")
client = OllamaClient()


class ChatRequest(BaseModel):
    message: str
    temperature: float = 0.2


class ChatResponse(BaseModel):
    reply: str
    model: str


@app.get("/health")
def health():
    return {"status": "ok", "model": client.config.model, "ollama_url": client.config.base_url}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = client.chat_text(
        messages=[{"role": "user", "content": request.message}],
        temperature=request.temperature,
    )
    return ChatResponse(reply=reply, model=client.config.model)
