import requests
import os

GUVI_URL = os.getenv("GUVI_CALLBACK_URL")

def send_final_result(session_id, session):

    intel = session["intelligence"]

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": session["total_messages"],
        "extractedIntelligence": {
            "bankAccounts": intel.bankAccounts,
            "upiIds": intel.upiIds,
            "phishingLinks": intel.phishingLinks,
            "phoneNumbers": intel.phoneNumbers,
            "suspiciousKeywords": intel.suspiciousKeywords
        },
        "agentNotes": intel.agentNotes or "Scammer used urgency and payment redirection"
    }

    try:
        requests.post(GUVI_URL, json=payload, timeout=5)
    except:
        pass
