from fastapi import FastAPI

from app.db import create_db_and_tables
from app.routers import chat

app = FastAPI(title="AI Self-Growth Coach API")


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


app.include_router(chat.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
