from fastapi import APIRouter, HTTPException
from app.models.schemas import HoneypotRequest, HoneypotResponse
from app.services.orchestrator import handle_message

router = APIRouter()

@router.post("/message", response_model=HoneypotResponse)
def honeypot_message(request: HoneypotRequest):
    try:
        reply = handle_message(request)
        return HoneypotResponse(status="success", reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
