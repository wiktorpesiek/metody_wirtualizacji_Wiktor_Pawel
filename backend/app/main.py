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



@app.get("/listings")
def search_listings(
    q: str | None = Query(None, max_length=100),
    category_id: int | None = None,
    city: str | None = None,
    min_price: Decimal | None = Query(None, ge=0),
    max_price: Decimal | None = Query(None, ge=0),
    sort: Literal["newest", "price_asc", "price_desc"] = "newest",
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Lista ogłoszeń z filtrami. Każdy filtr = jeden warunek WHERE, wartości zawsze przez %s."""
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(400, "min_price nie może być większe niż max_price")

    where, params = [], []
    if q:
        where.append("(title ILIKE %s OR description ILIKE %s)")
        params += [f"%{q}%", f"%{q}%"]
    if category_id is not None:
        where.append("category_id = %s")
        params.append(category_id)
    if city:
        where.append("city ILIKE %s")
        params.append(city)
    if min_price is not None:
        where.append("price >= %s")
        params.append(min_price)
    if max_price is not None:
        where.append("price <= %s")
        params.append(max_price)

    sql = f"SELECT {COLUMNS} FROM listings"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += f" ORDER BY {SORTS[sort]} LIMIT %s OFFSET %s"
    params += [limit, offset]

    with get_conn() as conn:
        return conn.execute(sql, params).fetchall()