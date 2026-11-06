# Advanced integrations
- LangGraph: actual directed workflow is implemented in `app/workflow.py`.
- JWT authentication: register/login routes and protected API dependency are implemented. Enable with `AUTH_ENABLED=true`, set a unique strong `JWT_SECRET`. The included frontend demo does not yet provide a login screen; use API docs/curl or build UI auth before enabling it in the browser.
- pgvector: SQL schema and helper are included. Configure PostgreSQL + pgvector and populate embeddings before using vector retrieval. The default app retrieval is keyword-based for portable zero-cost SQLite use.
- Sentence Transformers: `embed_text()` downloads all-MiniLM-L6-v2 on first use; local inference after download.
- RAGAS: evaluation harness is included but needs an evaluator LLM and dataset tuning; not part of runtime.
- Langfuse: optional tracing adapter uses credentials if configured; otherwise silently disabled.
- MCP: `mcp_server.py` exposes read-only incident tools. Start from backend folder after installing requirements.
These components have different readiness levels; see Tamil guide. No integration is represented as production-certified.
