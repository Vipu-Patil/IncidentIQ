"""
Raw Ollama client — Phase 4 territory: talk to the LLM directly,
no LangChain, no LangGraph. Understand every parameter before any
framework hides it from you.

Ollama exposes an OpenAI-incompatible-but-simple REST API on
http://localhost:11434 by default. Two endpoints matter here:

  POST /api/chat      -> multi-turn chat, takes a list of messages
  POST /api/generate  -> single prompt completion (less used here)

Docs: https://github.com/ollama/ollama/blob/main/docs/api.md
"""

import os
import httpx
from dotenv import load_dotenv
load_dotenv()
from dataclasses import dataclass
from typing import Optional



@dataclass
class OllamaConfig:
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    timeout_seconds: float = 120.0


class OllamaClient:
    """Thin wrapper. Deliberately un-abstracted so you can see every field."""

    def __init__(self, config: Optional[OllamaConfig] = None):
        self.config = config or OllamaConfig()

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.2,
        max_tokens: int = 512,
        system: Optional[str] = None,
    ) -> dict:
        """
        messages: [{"role": "user"|"assistant"|"system", "content": "..."}]
        Returns the raw parsed JSON response from Ollama.
        """
        payload_messages = list(messages)
        if system:
            payload_messages = [{"role": "system", "content": system}] + payload_messages

        payload = {
            "model": self.config.model,
            "messages": payload_messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        with httpx.Client(timeout=self.config.timeout_seconds) as client:
            response = client.post(f"{self.config.base_url}/api/chat", json=payload)
            response.raise_for_status()
            return response.json()

    def chat_text(self, messages: list[dict], **kwargs) -> str:
        """Convenience: return just the assistant's text content."""
        result = self.chat(messages, **kwargs)
        return result.get("message", {}).get("content", "")


if __name__ == "__main__":
    # Quick manual smoke test: python -m llm.ollama_client
    client = OllamaClient()
    reply = client.chat_text(
        messages=[{"role": "user", "content": "Say hello in exactly five words."}]
    )
    print("Model replied:", reply)
