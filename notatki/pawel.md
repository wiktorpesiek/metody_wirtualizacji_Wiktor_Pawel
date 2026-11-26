   ## Zajęcia 1 - 26.10.2026 — Paweł
   **Zrobione:** założone repo, dodany współpracownik, sklonowane repo
   **Problemy i rozwiązanie:** brak
   **Commity:** (236cc6e, 2f14a2c, 42c0477)
   **Na następne zajęcia:** init.sql i backend (FastAPI)

   
## Zajęcia 2 — 05.11.2026 — Paweł
**Zrobione:** .env.example (wzór zmiennych środowiskowych, hasło tylko w lokalnym .env) i .gitattributes (końce linii LF). Frontend w Streamlit: Dockerfile, requirements.txt, app.py pobierający listę ogłoszeń z backendu przez HTTP i wyświetlający ją w tabeli. docker-compose.yml: 3 kontenery (db, backend, frontend), sieci frontnet i backnet, wolumen db_data, healthcheck bazy. README: architektura, instrukcja uruchomienia, zmienne środowiskowe, tabela użycia AI. Uruchomione 3 kontenery, frontend pokazuje dane z bazy.
**Problemy i rozwiązanie:** brak
**Commity:** (wynik: c455d7f (HEAD -> main, origin/main, origin/HEAD) Edycja README: architektura, instrukcja uruchomienia i zmienne środowiskowe
5ef09b1 Compose z dwiema sieciami, wolumenem i healthcheckiem
92371e4 Frontend, Streamlit pobiera listę ogłoszeń z backendu
8cf3685 Wzór zmiennych środowiskowych i końce linii LF
e787dd7  endpointy /health i /listings z bazy)

## Zajęcia 3 — 24.11.2026 — Paweł
**Zrobione:** pokaz KM1: 3 kontenery, frontend → backend → baza, izolacja sieci, trwałość danych; pokaz awarii bazy na prośbę prowadzącego
**Ujawnione wymagania backendu:** min. 4 endpointy (GET pojedynczy, GET lista, POST, PUT/PATCH lub DELETE); JSON udokumentowany w README; walidacja (400); 404 dla nieistniejącego zasobu; /health; healthcheck w compose na /health + depends_on: service_healthy; konfiguracja przez zmienne środowiskowe
**Problemy i rozwiązanie:** zatrzymanie bazy dawało 500 na froncie → backend zwraca 503, frontend rozróżnia awarię bazy i backendu
**Na następne zajęcia:** implementacja API

## Zajęcia 4 — 26.11.2026 — Paweł
**Zrobione:** (healthcheck backendu na /health + depends_on service_healthy, PUT i DELETE z 404)
**Problemy i rozwiązanie:** (np. PowerShell psuł JSON w curl → dane w plikach scripts/*.json)

## Zajęcia 5 — 26.11.2026 — Paweł
**Zrobione:** (testy zapisu test_write.py, dokumentacja API w README)
**Problemy i rozwiązanie:** (np. testy wymagają przebudowy obrazu, bo kod jest kopiowany przy buildzie)
**Na następne zajęcia:** pokaz KM2
