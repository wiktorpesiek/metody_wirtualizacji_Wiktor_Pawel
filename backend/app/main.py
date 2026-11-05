from fastapi import FastAPI

from app.db import get_conn

app = FastAPI(title="Mini Marketplace API")


@app.get("/health")
def health():
    with get_conn() as conn:
        conn.execute("SELECT 1")
    return {"status": "ok"}


@app.get("/listings")
def list_listings():
    with get_conn() as conn:
        return conn.execute(
            "SELECT id, title, price, city, created_at FROM listings ORDER BY created_at DESC"
        ).fetchall()