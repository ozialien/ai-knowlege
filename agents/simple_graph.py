from typing import TypedDict
from langgraph.graph import StateGraph, END
from apps.api.ollama_client import chat

class AgentState(TypedDict):
    task: str
    plan: str
    answer: str

async def planner(state: AgentState) -> AgentState:
    plan = await chat(f"Create a short plan for this task: {state['task']}")
    state["plan"] = plan
    return state

async def responder(state: AgentState) -> AgentState:
    answer = await chat(
        f"Task: {state['task']}\nPlan: {state['plan']}\nProvide a concise useful answer."
    )
    state["answer"] = answer
    return state

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("planner", planner)
    graph.add_node("responder", responder)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "responder")
    graph.add_edge("responder", END)
    return graph.compile()
