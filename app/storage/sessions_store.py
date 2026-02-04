from typing import Dict
from app.models.intelligence_models import Intelligence

# In-memory session store
_SESSIONS: Dict[str, dict] = {}


def get_session(session_id: str) -> dict:
    """
    Load or create a session.
    """
    if session_id not in _SESSIONS:
        _SESSIONS[session_id] = {
            "messages": [],
            "intelligence": Intelligence(),
            "completed": False,
            "total_messages": 0,
        }

    return _SESSIONS[session_id]


def save_session(session_id: str, session: dict):
    """
    Persist session (noop for in-memory).
    """
    _SESSIONS[session_id] = session
