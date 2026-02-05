from typing import Dict
from app.models.intelligence_models import Intelligence

_SESSIONS: Dict[str, dict] = {}

def get_session(session_id: str) -> dict:
    if session_id not in _SESSIONS:
        _SESSIONS[session_id] = {
            "messages": [],
            "intelligence": Intelligence(),
            "completed": False,
            "total_messages": 0,
            "scamDetected": False,
            "agentNotes": "",
            "final_sent": False
        }

    return _SESSIONS[session_id]

def save_session(session_id: str, session: dict):
    _SESSIONS[session_id] = session
