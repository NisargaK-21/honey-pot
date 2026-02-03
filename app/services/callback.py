import requests
import os

GUVI_URL = os.getenv("GUVI_CALLBACK_URL")

def send_final_result(session_id, session):
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": len(session["messages"]),
        "extractedIntelligence": session["intelligence"],
        "agentNotes": session.get("agentNotes", "")
    }

    try:
        requests.post(
            GUVI_URL,
            json=payload,
            timeout=5
        )
    except Exception:
        pass  
