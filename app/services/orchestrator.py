from app.services.scam_detector import detect_scam
from app.services.agent import generate_reply
from app.services.intelligence import extract_intelligence
from app.services.callback import send_final_result
from app.storage.sessions_store import get_session, save_session

def handle_message(request):
    session_id = request.sessionId

    session = get_session(session_id)

    reply_text="Okay"

    session["messages"].append(request.message.dict())
    session["total_messages"] += 1

    scam_result = detect_scam(request.message.text, request.message.sender)

    reply_payload = {
        "scamDetected": scam_result["scamDetected"],
        "confidence": scam_result["confidenceScore"],
        "scam_type": scam_result["scamType"],
        "analysis": ", ".join(scam_result["reasons"]),
        "recommended_action": "Ignore message",
        "reply_text": reply_text
    }

    if scam_result["scamDetected"]:
        reply_text = generate_reply(
            message=request.message.text,
            history=session["messages"]
        )

        reply_payload["reply_text"] = reply_text

        extract_intelligence(
            text=request.message.text,
            intelligence=session["intelligence"]
        )

        from app.services.intelligence import update_agent_notes
        update_agent_notes(session["intelligence"])

        reply_payload["recommended_action"] = "Block sender and report to bank"

        if session["total_messages"] >= 5:
            session["completed"] = True

    save_session(session_id, session)

    if session["completed"]:
        send_final_result(session_id, session)

    return reply_payload
