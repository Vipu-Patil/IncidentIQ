# AgentForge Open-Source Dataset

This dataset is designed for an AI incident-investigation agent.

## Three core datasets

1. `incidents/` — investigation inputs: incidents, logs, metrics, deployments,
   source/context, and ground-truth resolutions.
2. `knowledge_base/` — RAG corpus containing architecture, services, runbooks,
   deployment rules, and security policies.
3. `evaluation/` — benchmark cases for measuring root-cause accuracy, evidence
   handling, and safety behavior.

`finetuning/` is optional and can be used later for LoRA/QLoRA experiments.

## Recommended ingestion

- Parse incident files into PostgreSQL.
- Chunk Markdown files from `knowledge_base/`.
- Generate embeddings with an open-source embedding model.
- Store vectors in PostgreSQL + pgvector.
- Keep incident ground truth outside the production retrieval index so evaluation
  does not leak answers.
- Use evaluation cases only in the evaluation pipeline.

## Suggested open-source stack

LLM: Qwen / Llama / Mistral via Ollama or vLLM
Embeddings: BGE / E5 / Nomic
Vector database: PostgreSQL + pgvector
Backend: FastAPI
Agent orchestration: LangGraph
Frontend: React + TypeScript
Observability: OpenTelemetry + Prometheus + Grafana
Deployment: Docker + Kubernetes

## Important evaluation rule

Do NOT index `ground_truth_root_cause` and `expected_resolution` into the same
retrieval corpus used by the agent. Otherwise the benchmark leaks the answer.
