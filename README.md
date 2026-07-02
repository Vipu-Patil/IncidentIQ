# AgentForge

An AI incident-investigation agent. Given a production incident (logs,
metrics, deployments, code context), it investigates and produces an
evidence-backed root-cause report — first as a raw LLM call, later as a
LangGraph agent with tools and RAG.

Stack: Ollama (local open-source LLM) → FastAPI → RAG (Postgres+pgvector) →
LangGraph agent → LangSmith-style evaluation. Built in that order, on purpose —
see `data/DATASET_README.md` for the dataset rules.

## Where things stand (Day 1)

- [x] Project scaffolded
- [x] Dataset wired in under `data/`
- [x] Raw Ollama client (`llm/ollama_client.py`) — no framework
- [x] Smoke test proving the model can read one incident and reason about it
- [x] Minimal FastAPI app exposing `/health` and `/chat`
- [ ] RAG over `data/knowledge_base/` (next)
- [ ] Tool calling over logs/metrics/deployments (next)
- [ ] LangGraph agent
- [ ] Evaluation against `data/evaluation/benchmark.jsonl`

## Setup

### 1. Install and start Ollama

Download from https://ollama.com if you don't have it yet, then pull a model:

```bash
ollama pull qwen2.5:7b
```

(Any reasonably capable instruct model works — `llama3.1:8b` or `mistral:7b`
are fine substitutes. Just keep `.env`'s `OLLAMA_MODEL` matching whatever you
pulled.)

Ollama runs as a background service automatically after install, listening on
`http://localhost:11434`.

### 2. Python environment

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment variables

```bash
cp .env.example .env
```

Edit `.env` if your model name differs from the default.

### 4. Start Postgres (only needed from the RAG phase onward, but fine to start now)

```bash
docker compose up -d
```

### 5. Run the Day-1 smoke test

```bash
python scripts/test_llm_connection.py
```

This loads `INC-001` from the dataset, sends its logs/metrics to your local
model with a raw prompt (no framework), and prints the model's root-cause
guess next to the real ground truth — so you can see how close a bare LLM
call gets before any RAG or tooling is added.

### 6. Run the API

```bash
uvicorn backend.main:app --reload
```

Visit `http://localhost:8000/docs` and try `/health` then `/chat`.

## Project layout

```
agentforge/
├── backend/           FastAPI app
├── llm/                Raw Ollama client (Phase 4 — no framework)
├── scripts/            One-off scripts, smoke tests
├── notebooks/          Scratchpad only — nothing here ships
├── data/
│   ├── incidents/       8 incidents (INC-001..008), including a prompt-
│   │                      injection case (INC-007) and a human-approval
│   │                      case (INC-008)
│   ├── knowledge_base/   RAG corpus: architecture, services, runbooks,
│   │                      deployment, security
│   ├── evaluation/       benchmark.jsonl — root-cause accuracy tests
│   ├── finetuning/       optional, for later LoRA/QLoRA experiments
│   └── DATASET_README.md
├── tests/
├── docker-compose.yml   Postgres + pgvector
├── requirements.txt
└── .env.example
```

## Important rule (from the dataset README — do not skip this)

`ground_truth_root_cause` and `expected_resolution` inside `incidents/*/incident.json`
must **never** be fed to the model or indexed into the RAG corpus. They exist
only so *you* can grade the agent's output. The smoke test script deliberately
excludes them from the prompt — keep that pattern everywhere else too, or the
benchmark becomes meaningless.
