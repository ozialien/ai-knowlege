from fastapi import FastAPI
from pydantic import BaseModel
from agents.retrieval_agent import handle as retrieval_handle
from agents.code_agent import handle as code_handle
from agents.ops_agent import handle as ops_handle

app = FastAPI(title="AI Platform V6 Multi-Agent", version="0.6.0")

class TaskRequest(BaseModel):
    task_type: str
    payload: dict

@app.get("/health")
def health():
    return {"status": "ok", "agents": ["retrieval", "code", "ops"]}

@app.post("/dispatch")
def dispatch(req: TaskRequest):
    if req.task_type == "retrieval":
        return retrieval_handle(req.payload)
    if req.task_type == "code":
        return code_handle(req.payload)
    if req.task_type == "ops":
        return ops_handle(req.payload)
    return {"error": f"Unknown task type: {req.task_type}"}
