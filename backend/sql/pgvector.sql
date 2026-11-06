CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS knowledge_vectors (
  id BIGSERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  embedding vector(384) NOT NULL
);
CREATE INDEX IF NOT EXISTS knowledge_vectors_embedding_idx
ON knowledge_vectors USING hnsw (embedding vector_cosine_ops);
