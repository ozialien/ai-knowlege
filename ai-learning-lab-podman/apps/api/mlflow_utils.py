import mlflow
from apps.api.config import settings

mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
mlflow.set_experiment("ai-learning-lab")

def log_event(event_type: str, payload: dict):
    with mlflow.start_run(nested=True):
        mlflow.log_param("event_type", event_type)
        for key, value in payload.items():
            if isinstance(value, (str, int, float, bool)):
                mlflow.log_param(key, value)
