from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()   # 👈 THIS LINE FIXES EVERYTHING

from app.routes.honeypot import router as honeypot_router

app = FastAPI(title="Agentic Honeypot API")

app.include_router(honeypot_router, prefix="/honeypot")

@app.get("/")
def health_check():
    return {"status": "ok"}
