"""Optional pgvector helper. PostgreSQL must have CREATE EXTENSION vector enabled.
SQLite uses the transparent keyword retrieval baseline in engine.py."""
import os
def pgvector_search(query_embedding, limit=5):
    url=os.getenv("DATABASE_URL","")
    if not url.startswith(("postgresql://","postgresql+psycopg://")):
        raise RuntimeError("pgvector search requires PostgreSQL; SQLite fallback uses keyword retrieval.")
    from sqlalchemy import create_engine, text
    engine=create_engine(url)
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        # Demo schema uses 384-dim all-MiniLM-L6-v2 embeddings.
        conn.execute(text("CREATE TABLE IF NOT EXISTS knowledge_vectors (id SERIAL PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL, embedding vector(384) NOT NULL)"))
        literal="["+(",".join(str(float(v)) for v in query_embedding))+"]"
        rows=conn.execute(text("SELECT id,title,content FROM knowledge_vectors ORDER BY embedding <=> CAST(:v AS vector) LIMIT :n"),{"v":literal,"n":limit}).mappings().all()
        return [dict(x) for x in rows]
def embed_text(text_value:str):
    from sentence_transformers import SentenceTransformer
    model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return model.encode(text_value,normalize_embeddings=True).tolist()
