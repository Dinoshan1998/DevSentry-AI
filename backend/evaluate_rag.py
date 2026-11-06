"""Optional RAGAS evaluation harness. Requires an LLM configured for RAGAS.
Run after setting up a supported RAGAS evaluator; this script is intentionally
not run during normal application startup."""
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
samples={"question":["What should I inspect for database connection refused?"],"answer":["Check database service health, hostname, port and connection pool."],"contexts":[["Database runbook: inspect service health, hostname, port and pool saturation."]],"ground_truth":["Inspect database health, host, port and pool saturation."]}
dataset=Dataset.from_dict(samples)
print(evaluate(dataset,metrics=[faithfulness,answer_relevancy]))
