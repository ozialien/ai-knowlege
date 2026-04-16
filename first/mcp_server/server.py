import json
import sys
from mcp_server.tools import list_tools, call_tool

def handle_message(message: dict) -> dict:
    method = message.get("method")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": message.get("id"), "result": {"tools": list_tools()}}
    if method == "tools/call":
        params = message.get("params", {})
        name = params.get("name")
        arguments = params.get("arguments", {})
        return {"jsonrpc": "2.0", "id": message.get("id"), "result": call_tool(name, arguments)}
    return {"jsonrpc": "2.0", "id": message.get("id"), "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        req = json.loads(line)
        res = handle_message(req)
        sys.stdout.write(json.dumps(res) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
