from app.services.scam_detector import detect_scam
from app.services.agent import generate_reply
from app.services.intelligence import extract_intelligence
from app.services.callback import send_final_result
from app.storage.sessions_store import get_session, save_session

def handle_message(request):
    session_id = request.sessionId
    session = get_session(session_id)

    session["messages"].append(request.message.dict())

    scam_result = detect_scam(request.message.text)

    reply = "Okay."

    if scam_result["scamDetected"]:
        reply = generate_reply(
            message=request.message.text,
            history=session["messages"]
        )

        extract_intelligence(
            text=request.message.text,
            intelligence=session["intelligence"]
        )

    save_session(session_id, session)


    if scam_result["scamDetected"] and session.get("completed"):
        send_final_result(session_id, session)

    return reply
