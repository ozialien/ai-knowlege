from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from apps.api.ollama_client import chat, embed
from apps.api.config import settings
from apps.api.mlflow_utils import log_event
from apps.api.lesson_notes import LESSONS
from rag.pipeline import build_records_from_path
from rag.qdrant_store import upsert_records, search
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from mcp_server.tools import list_tools, call_tool
from multi_agent.coordinator import dispatch_task

app = FastAPI(title="AI Learning Lab", version="1.0.0")

class ChatRequest(BaseModel):
    message: str
    system: str | None = "You are a concise local AI assistant."

class QuestionRequest(BaseModel):
    question: str
    top_k: int = 5

class AgentRequest(BaseModel):
    task: str
    thread_id: str | None = None

class DispatchRequest(BaseModel):
    name: str
    arguments: dict = {}

def build_graph():
    async def planner(state: dict) -> dict:
        state["plan"] = await chat(f"Create a short plan for this task: {state['task']}")
        return state
    async def responder(state: dict) -> dict:
        state["answer"] = await chat(
            f"Task: {state['task']}\\nPlan: {state['plan']}\\nProvide a concise useful answer."
        )
        return state
    graph = StateGraph(dict)
    graph.add_node("planner", planner)
    graph.add_node("responder", responder)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "responder")
    graph.add_edge("responder", END)
    return graph.compile(checkpointer=MemorySaver())

graph = build_graph()

@app.get("/lesson")
def lesson_index():
    return LESSONS

@app.get("/lesson/00/health")
def health():
    return {
        "status": "ok",
        "lessons": LESSONS,
        "chat_model": settings.ollama_chat_model,
        "embed_model": settings.ollama_embed_model,
    }

@app.post("/lesson/01/chat")
async def lesson_01_chat(req: ChatRequest):
    response = await chat(req.message, req.system)
    log_event("chat", {"lesson": "01"})
    return {"lesson": "01", "response": response}

@app.post("/lesson/02/embed")
async def lesson_02_embed(req: ChatRequest):
    vectors = await embed([req.message])
    log_event("embed", {"lesson": "02", "count": len(vectors)})
    return {"lesson": "02", "vector_dimensions": len(vectors[0]) if vectors else 0}

@app.post("/lesson/03/ingest_examples")
async def lesson_03_ingest_examples():
    records = build_records_from_path("/app/data/examples", "examples")
    if not records:
        raise HTTPException(status_code=400, detail="No example records found")
    vectors = await embed([r["text"] for r in records])
    count = upsert_records(records, vectors)
    log_event("ingest", {"lesson": "03", "count": count})
    return {"lesson": "03", "records_indexed": count}

@app.post("/lesson/03/rag_answer")
async def lesson_03_rag_answer(req: QuestionRequest):
    query_vec = (await embed([req.question]))[0]
    results = search(query_vec, top_k=req.top_k)
    contexts = [r.get("text", "") for r in results]
    answer = await chat(
        "Answer using only the provided context. If the answer is not present, say so.\\n\\n"
        f"Question: {req.question}\\n\\nContext:\\n" + "\\n---\\n".join(contexts),
        "You are a grounded RAG assistant."
    )
    citations = [{
        "title": r.get("title", ""),
        "path": r.get("path", ""),
        "chunk_index": r.get("chunk_index", -1),
        "source": r.get("source", ""),
    } for r in results]
    log_event("rag", {"lesson": "03", "contexts": len(contexts)})
    return {"lesson": "03", "answer": answer, "citations": citations}

@app.post("/lesson/04/agent_run")
async def lesson_04_agent_run(req: AgentRequest):
    thread_id = req.thread_id or settings.langgraph_thread_id
    result = await graph.ainvoke(
        {"task": req.task, "plan": "", "answer": ""},
        config={"configurable": {"thread_id": thread_id}},
    )
    log_event("agent", {"lesson": "04", "thread_id": thread_id})
    return {"lesson": "04", "thread_id": thread_id, **result}

@app.get("/lesson/05/mcp_tools")
def lesson_05_mcp_tools():
    return {"lesson": "05", "tools": list_tools()}

@app.post("/lesson/05/mcp_call")
def lesson_05_mcp_call(req: DispatchRequest):
    return {"lesson": "05", "result": call_tool(req.name, req.arguments)}

@app.post("/lesson/06/dispatch")
def lesson_06_dispatch(req: DispatchRequest):
    return {"lesson": "06", "result": dispatch_task(req.name, req.arguments)}
