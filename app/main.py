from fastapi import FastAPI
from app.routes.honeypot import router as honeypot_router
from app.utils.auth import verify_api_key

app = FastAPI(title="Agentic Honeypot API")


app.include_router(honeypot_router, prefix="/honeypot")

@app.get("/")
def health_check():
    return {"status": "ok"}
