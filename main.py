from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "ok",
        "database_url_present": bool(os.getenv("DATABASE_URL")),
    }