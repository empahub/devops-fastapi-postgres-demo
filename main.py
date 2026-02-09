import os
import asyncpg
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")


class NoteIn(BaseModel):
    text: str


@app.on_event("startup")
async def startup():
    app.state.pool = await asyncpg.create_pool(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    async with app.state.pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL
            );
        """)


@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/notes")
async def get_notes():
    async with app.state.pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, text FROM notes ORDER BY id;")
        return [{"id": r["id"], "text": r["text"]} for r in rows]


@app.post("/notes")
async def create_note(note: NoteIn):
    async with app.state.pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO notes(text) VALUES($1) RETURNING id, text;", note.text
        )
        return {"id": row["id"], "text": row["text"]}

