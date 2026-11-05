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
