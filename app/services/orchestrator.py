from app.services.scam_detector import detect_scam
from app.services.agent import generate_reply
from app.services.intelligence import extract_intelligence, update_agent_notes
from app.services.callback import send_final_result
from app.storage.sessions_store import get_session, save_session

def handle_message(request):

    session_id = request.sessionId

    session = get_session(session_id)

    session["messages"].append(request.message.dict())

    scam_result = detect_scam(request.message.text)

    reply_payload = scam_result

    if scam_result["scamDetected"]:

        extract_intelligence(
            text=request.message.text,
            intelligence=session["intelligence"]
        )

        update_agent_notes(session["intelligence"])

        reply_payload = scam_result

    save_session(session_id, session)

    if scam_result["scamDetected"] and session.get("completed"):
        send_final_result(session_id, session)

    return reply_payload
