import mlflow
from apps.api.config import settings

mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
mlflow.set_experiment("local-ai-platform")

def log_chat(message: str, response: str, model: str) -> None:
    with mlflow.start_run(nested=True):
        mlflow.log_param("type", "chat")
        mlflow.log_param("model", model)
        mlflow.log_text(message, "input.txt")
        mlflow.log_text(response, "response.txt")

def log_rag(question: str, answer: str, top_k: int, context_count: int) -> None:
    with mlflow.start_run(nested=True):
        mlflow.log_param("type", "rag")
        mlflow.log_param("top_k", top_k)
        mlflow.log_param("context_count", context_count)
        mlflow.log_text(question, "question.txt")
        mlflow.log_text(answer, "answer.txt")

def log_ingestion(source: str, count: int) -> None:
    with mlflow.start_run(nested=True):
        mlflow.log_param("type", "ingest")
        mlflow.log_param("source", source)
        mlflow.log_metric("chunks_indexed", count)
