from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from apps.api.ollama_client import chat

class AgentState(TypedDict):
    task: str
    plan: str
    answer: str

async def planner(state: AgentState) -> AgentState:
    state["plan"] = await chat(f"Create a short plan for this task: {state['task']}")
    return state

async def responder(state: AgentState) -> AgentState:
    state["answer"] = await chat(
        f"Task: {state['task']}\nPlan: {state['plan']}\nProvide a concise useful answer."
    )
    return state

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("planner", planner)
    graph.add_node("responder", responder)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "responder")
    graph.add_edge("responder", END)
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)
