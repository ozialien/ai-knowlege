def handle(payload: dict):
    question = payload.get("question", "")
    return {"agent": "retrieval", "question": question, "result": f"Stub retrieval answer for: {question}"}
