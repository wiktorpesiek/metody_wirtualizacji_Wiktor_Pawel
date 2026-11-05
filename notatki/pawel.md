   ## Zajęcia 1 - 26.10.2026 — Paweł
   **Zrobione:** założone repo, dodany współpracownik, sklonowane repo
   **Problemy i rozwiązanie:** brak
   **Commity:** (236cc6e, 2f14a2c, 42c0477)
   **Na następne zajęcia:** init.sql i backend (FastAPI)

   
## Zajęcia 2 — DD.MM.2026 — Paweł
**Zrobione:** .env.example (wzór zmiennych środowiskowych, hasło tylko w lokalnym .env) i .gitattributes (końce linii LF). Frontend w Streamlit: Dockerfile, requirements.txt, app.py pobierający listę ogłoszeń z backendu przez HTTP i wyświetlający ją w tabeli. docker-compose.yml: 3 kontenery (db, backend, frontend), sieci frontnet i backnet, wolumen db_data, healthcheck bazy. README: architektura, instrukcja uruchomienia, zmienne środowiskowe, tabela użycia AI. Uruchomione 3 kontenery, frontend pokazuje dane z bazy.
**Problemy i rozwiązanie:** brak
**Commity:** (wynik: c455d7f (HEAD -> main, origin/main, origin/HEAD) Edycja README: architektura, instrukcja uruchomienia i zmienne środowiskowe
5ef09b1 Compose z dwiema sieciami, wolumenem i healthcheckiem
92371e4 Frontend, Streamlit pobiera listę ogłoszeń z backendu
8cf3685 Wzór zmiennych środowiskowych i końce linii LF
e787dd7  endpointy /health i /listings z bazy)
**Na następne zajęcia:** pokaz KM1, przećwiczenie odpowiedzi na pytania o sieci, wolumen i compose