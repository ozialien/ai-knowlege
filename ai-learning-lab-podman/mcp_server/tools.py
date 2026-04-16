def list_tools():
    return [
        {
            "name": "health_check",
            "description": "Return local service health",
            "input_schema": {"type": "object", "properties": {}},
        },
        {
            "name": "retrieve_docs",
            "description": "Retrieve docs by query from a future RAG tool boundary",
            "input_schema": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    ]

def call_tool(name: str, arguments: dict):
    if name == "health_check":
        return {"content": [{"type": "text", "text": "Local platform is healthy"}]}
    if name == "retrieve_docs":
        return {"content": [{"type": "text", "text": f"Stub retrieval for query: {arguments.get('query', '')}"}]}
    raise ValueError(f"Unknown tool: {name}")
