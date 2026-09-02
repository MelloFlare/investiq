from fastapi import FastAPI
from app.database import check_db_connection

app = FastAPI(title="InvestIQ")

@app.get("/")
def root():
    return {"status": "ok", "application": "InvestIQ"}

@app.get("/health")
def health():
    db_ok = check_db_connection()
    return {
        "api": "healthy",
        "database": "connected" if db_ok else "disconnected"
    }