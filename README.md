# Mini Marketplace - ogłoszenia z wyszukiwarką
Projekt z Metod Wirtualizacji, PP WIiT, 2026/2027.
Autorzy: Wiktor Pęsiek, Paweł Czarnecki

# Architektura
frontend (Streamlit, :8501) -> backend (FastAPI, :8000) -> db (PostgreSQL 16)

- Sieć “frontnet:” frontend, backend
- Sieć “backnet”: backend, db
- Frontend nie ma dostępu do bazy, rozmawia wyłącznie z backendem (HTTP + JSON).
- Dane bazy w wolumenie “db_data”, przeżywają restart kontenerów.


# Uruchomienie
Copy-Item .env.example .env
w pliku .env ustawione własne POSTGRES_PASSWORD
docker compose up --build -d
docker compose ps
- Frontend: http://localhost:8501
- API: http://localhost:8000/listings
- Dokumentacja API: http://localhost:8000/docs

Zatrzymanie: “docker compose down” (dane zostają), “docker compose down -v” (kasuje dane).

# Zmienne środowiskowe
| Zmienna | Opis | Kto używa |
| POSTGRES_USER | użytkownik bazy | db, backend |
| POSTGRES_PASSWORD | hasło bazy (tylko w .env, poza repo) | db, backend |
| POSTGRES_DB | nazwa bazy | db, backend |
| DB_HOST / DB_PORT | adres bazy w sieci Dockera | backend |
| BACKEND_URL | adres backendu | frontend |

## API

Bazowy adres: `http://localhost:8000`. Format wymiany danych: JSON (`Content-Type: application/json`).
Interaktywna dokumentacja: `http://localhost:8000/docs`.

| Metoda | Ścieżka | Opis | Sukces | Błędy |
| --- | --- | --- | --- | --- |
| GET | `/health` | stan backendu i połączenia z bazą | 200 | 503 baza niedostępna |
| GET | `/listings` | lista ogłoszeń z wyszukiwarką | 200 | 400 błędne parametry |
| GET | `/listings/{id}` | jedno ogłoszenie | 200 | 400 zły typ id, 404 brak ogłoszenia |
| GET | `/categories` | lista kategorii | 200 | — |
| POST | `/listings` | dodanie ogłoszenia | 201 | 400 błędne dane lub nieistniejąca kategoria |
| PUT | `/listings/{id}` | pełna aktualizacja ogłoszenia | 200 | 400, 404 |
| DELETE | `/listings/{id}` | usunięcie ogłoszenia | 204 | 404 |

Każdy endpoint zwraca 503 `{"detail": "Baza danych niedostępna"}`, gdy baza nie odpowiada.

### Parametry wyszukiwania `GET /listings`

| Parametr | Typ | Opis |
| --- | --- | --- |
| `q` | tekst (max 100) | fraza w tytule lub opisie, bez rozróżniania wielkości liter |
| `category_id` | liczba | tylko dana kategoria |
| `city` | tekst | tylko dane miasto |
| `min_price`, `max_price` | liczba ≥ 0 | przedział cen; `min_price` > `max_price` → 400 |
| `sort` | `newest` / `price_asc` / `price_desc` | kolejność, domyślnie `newest` |
| `limit` | 1–100 | liczba wyników, domyślnie 20 |
| `offset` | ≥ 0 | przesunięcie (stronicowanie), domyślnie 0 |

Przykład: `GET /listings?q=rower&max_price=1000&sort=price_asc`

### Ogłoszenie — dane wejściowe (POST, PUT)

```json
{
  "title": "Laptop Dell Latitude",
  "description": "16 GB RAM, SSD 512 GB",
  "price": 2100,
  "city": "Poznań",
  "category_id": 1
}
```

| Pole | Wymagane | Reguły |
| --- | --- | --- |
| `title` | tak | tekst, 3–200 znaków |
| `description` | nie | tekst, max 5000 znaków, domyślnie pusty |
| `price` | tak | liczba ≥ 0, max 2 miejsca po przecinku |
| `city` | nie | tekst, max 100 znaków |
| `category_id` | nie | id istniejącej kategorii |

### Ogłoszenie — odpowiedź

```json
{
  "id": 4,
  "title": "Laptop Dell Latitude",
  "description": "16 GB RAM, SSD 512 GB",
  "price": 2100.0,
  "city": "Poznań",
  "category_id": 1,
  "created_at": "2026-11-24T20:15:00.123456Z"
}
```

### Format błędów

404 / logiczne 400 / 503:
```json
{"detail": "Ogłoszenie nie istnieje"}
```

400 przy błędnych danych wejściowych:
```json
{
  "detail": "Błędne dane wejściowe",
  "errors": [
    {"field": "title", "message": "String should have at least 3 characters"},
    {"field": "price", "message": "Input should be greater than or equal to 0"}
  ]
}
```

### Przykłady curl

```bash
curl http://localhost:8000/listings/1
curl "http://localhost:8000/listings?q=rower&sort=price_asc"
curl -X POST http://localhost:8000/listings -H "Content-Type: application/json" \
     -d '{"title": "Laptop Dell", "price": 2100, "city": "Poznań", "category_id": 1}'
curl -X DELETE http://localhost:8000/listings/4
```

Na Windowsie (PowerShell): `curl.exe` i dane z pliku, np. `--data "@scripts/listing_ok.json"`.
Pełny pokaz wszystkich endpointów: `powershell -ExecutionPolicy Bypass -File .\scripts\demo.ps1`

## Testy

```
docker compose up --build -d backend
docker compose exec backend python -m pytest -v -p no:cacheprovider
```
19 testów: `backend/tests/test_read.py` (odczyt, wyszukiwarka, 404, walidacja) i `backend/tests/test_write.py` (POST, PUT, DELETE, walidacja).
