from multi_agent.retrieval_agent import handle as retrieval_handle
from multi_agent.code_agent import handle as code_handle
from multi_agent.ops_agent import handle as ops_handle

def dispatch_task(name: str, arguments: dict):
    if name == "retrieval":
        return retrieval_handle(arguments)
    if name == "code":
        return code_handle(arguments)
    if name == "ops":
        return ops_handle(arguments)
    return {"error": f"Unknown agent: {name}"}
