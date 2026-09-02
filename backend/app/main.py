from fastapi import FastAPI
from app.database import check_db_connection
from app.routes import portfolios

app = FastAPI(title="InvestIQ")
app.include_router(portfolios.router)

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