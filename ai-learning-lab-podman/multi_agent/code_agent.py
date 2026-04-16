def handle(payload: dict):
    repo_question = payload.get("repo_question", "")
    return {"agent": "code", "repo_question": repo_question, "result": f"Stub code analysis for: {repo_question}"}
