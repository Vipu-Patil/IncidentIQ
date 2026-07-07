"""
Day 1 smoke test.

Goal: prove three things work before writing a single line of
LangChain/LangGraph/RAG:
  1. Ollama is running and reachable
  2. The chosen model responds
  3. The model can reason (a little) over one real incident from
     your actual dataset, using a raw prompt you fully control

Run with:  python scripts/test_llm_connection.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from llm.ollama_client import OllamaClient  # noqa: E402

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_incident(incident_id: str) -> dict:
    incident_dir = DATA_DIR / "incidents" / incident_id
    incident = json.loads((incident_dir / "incident.json").read_text())
    logs = (incident_dir / "logs.txt").read_text()
    metrics_path = incident_dir / "metrics.csv"
    metrics = metrics_path.read_text() if metrics_path.exists() else "(no metrics file)"
    return {"incident": incident, "logs": logs, "metrics": metrics}


def build_prompt(data: dict) -> str:
    incident = data["incident"]
    # Deliberately NOT including ground_truth_root_cause / expected_resolution —
    # that's the evaluation answer key, not something the agent should ever see
    # at inference time. This is the rule called out in the dataset README.
    return f"""You are investigating a production incident.

Title: {incident['title']}
Severity: {incident['severity']}

Logs:
{data['logs']}

Metrics:
{data['metrics']}

Based only on the evidence above, what is the most likely root cause?
Answer in 2-3 sentences and cite which log lines or metrics support your conclusion."""


def main():
    client = OllamaClient()

    print(f"Connecting to Ollama at {client.config.base_url} using model '{client.config.model}'...")

    data = load_incident("INC-007")
    prompt = build_prompt(data)

    print("\n--- Prompt sent to model ---")
    print(prompt)

    reply = client.chat_text(messages=[{"role": "user", "content": prompt}])

    print("\n--- Model's answer ---")
    print(reply)

    print("\n--- Ground truth (for your own comparison only, never shown to the model) ---")
    print(data["incident"]["ground_truth_root_cause"])


if __name__ == "__main__":
    main()
