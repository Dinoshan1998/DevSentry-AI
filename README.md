# DevSentry AI — AI SRE / Incident Intelligence Platform

A portfolio-grade, local-first incident analysis application. React + FastAPI + SQLite, a real LangGraph multi-step workflow, optional local Ollama inference, JWT auth endpoints, pgvector integration helpers, RAGAS evaluation harness, optional Langfuse tracing and read-only MCP tools.

## Quick start (free, no API keys)
Backend: `cd backend` → create/activate venv → `pip install -r requirements.txt` → `uvicorn app.main:app --reload`
Frontend: `cd frontend` → `npm install` → `npm run dev`
Open http://localhost:5173. API docs http://localhost:8000/docs.

Optional heavy integrations: run `pip install -r requirements-advanced.txt` from the backend folder only when you need local embeddings, RAGAS or Langfuse. These packages can consume substantial disk/RAM.

## Honest feature status
- Implemented: React dashboard, FastAPI endpoints, SQLite persistence, LangGraph workflow, rule-based log classification, keyword runbook retrieval, optional Ollama local generation, approval recording, JWT register/login API, optional Langfuse trace adapter, MCP read-only tools, pgvector SQL/helper, RAGAS evaluation example.
- Not fully production-ready: browser login UI, vector ingestion/indexing lifecycle, production RAGAS evaluation with chosen evaluator, distributed tracing dashboards, deployment secrets/HTTPS/rate limiting/tenant isolation. Review `backend/README_ADVANCED.md` and Tamil guide.

## Docker
`docker compose up --build` then open http://localhost:8080. This is a local demonstration deployment.

## Security
Do not paste secrets or personal data into logs. Before public deployment: enable auth, change JWT secret, configure exact CORS origins, HTTPS, rate limits, backups, monitoring and persistent database storage. Human approval is required; the app does not run production remediation commands.
