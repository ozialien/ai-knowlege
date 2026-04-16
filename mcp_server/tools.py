def list_tools():
    return [
        {
            "name": "health_check",
            "description": "Return local service health",
            "input_schema": {"type": "object", "properties": {}},
        },
        {
            "name": "retrieve_docs",
            "description": "Retrieve example local documents",
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
        query = arguments.get("query", "")
        return {"content": [{"type": "text", "text": f"Stub retrieval for query: {query}"}]}
    raise ValueError(f"Unknown tool: {name}")
