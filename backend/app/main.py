from decimal import Decimal
from typing import Literal

import psycopg
from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from psycopg.errors import ForeignKeyViolation
from pydantic import BaseModel, Field

from app.db import get_conn

app = FastAPI(title="Mini Marketplace API")

# kolumny zwracane w odpowiedziach o ogłoszeniach
COLUMNS = "id, title, description, price, city, category_id, created_at"

# ORDER BY nie da się sparametryzować -> dozwolone tylko wartości z tej białej listy
SORTS = {
    "newest": "created_at DESC",
    "price_asc": "price ASC",
    "price_desc": "price DESC",
}


class ListingIn(BaseModel):
    """Dane ogłoszenia przysyłane przez klienta. Nie ufamy im -> walidujemy każde pole."""
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(default="", max_length=5000)
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    city: str | None = Field(default=None, max_length=100)
    category_id: int | None = None


#obsługa błędów 

@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    """Błędne dane wejściowe -> 400 z listą pól, które nie przeszły walidacji."""
    errors = [
        {"field": ".".join(str(part) for part in err["loc"][1:]), "message": err["msg"]}
        for err in exc.errors()
    ]
    return JSONResponse(status_code=400, content={"detail": "Błędne dane wejściowe", "errors": errors})


@app.exception_handler(psycopg.OperationalError)
async def db_unavailable(request: Request, exc: psycopg.OperationalError):
    """Baza nie odpowiada -> 503 zamiast ogólnego 500."""
    return JSONResponse(status_code=503, content={"detail": "Baza danych niedostępna"})


# ---------- endpointy ----------

@app.get("/health")
def health():
    with get_conn() as conn:
        conn.execute("SELECT 1")
    return {"status": "ok"}