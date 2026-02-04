from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import HoneypotRequest, HoneypotResponse
from app.services.orchestrator import handle_message
from app.utils.auth import verify_api_key  

router = APIRouter()

@router.post(
    "/message",
    response_model=HoneypotResponse,
    dependencies=[Depends(verify_api_key)] 
)
def honeypot_message(request: HoneypotRequest):
    try:
        reply = handle_message(request)
        return HoneypotResponse(status="success", reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
