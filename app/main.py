from fastapi import FastAPI, Request
from app.routes.honeypot import router as honeypot_router

app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/")
async def root_post(request: Request):
    return {"status": "ok"}


app.include_router(honeypot_router, prefix="/honeypot")
