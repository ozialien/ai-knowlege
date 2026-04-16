def handle(payload: dict):
    incident = payload.get("incident", "")
    return {
        "agent": "ops",
        "incident": incident,
        "result": f"Stub ops guidance for: {incident}",
        "approval_required": True
    }
