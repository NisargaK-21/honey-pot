from fastapi import FastAPI, Depends
from app.routes.honeypot import router as honeypot_router
from app.utils.auth import verify_api_key

app = FastAPI(title="Agentic Honey-Pot API")

@app.get("/")
def health_check():
    return {"status": "ok"}


app.include_router(
    honeypot_router,
    prefix="/honeypot",
    dependencies=[Depends(verify_api_key)]
)
