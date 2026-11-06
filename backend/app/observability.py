import os
def trace_event(name:str, metadata:dict):
    # Langfuse is optional; app remains usable without cloud credentials.
    if not os.getenv("LANGFUSE_PUBLIC_KEY") or not os.getenv("LANGFUSE_SECRET_KEY"): return
    try:
        from langfuse import Langfuse
        client=Langfuse()
        span=client.start_span(name=name,input=metadata)
        span.end()
        client.flush()
    except Exception:
        # Observability must never break incident analysis.
        return
