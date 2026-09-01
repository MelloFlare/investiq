from fastapi import FastAPI

app = FastAPI(title="InvestIQ")

@app.get("/")
def root():
    return {"status": "ok", "application": "InvestIQ"}