   ## Zajęcia 1 Wiktor
   **Zrobione:** założone repo, dodany współpracownik, sklonowane repo
   **Problemy i rozwiązanie:** brak
   **Commity:** (2f14a2c, 42c0477)
   **Na następne zajęcia:** init.sql i backend (FastAPI)

   
   ## Zajęcia 2 Wiktor
   **Zrobione:** init.sql (tabele categories, listings + dane testowe), backend FastAPI: Dockerfile, połączenie z bazą, /health, /listings. Uruchomione 3 kontenery, frontend pokazuje dane z bazy.
   **Problemy i rozwiązanie:** brak
   **Commity:** (c455d7f (HEAD -> main, origin/main, origin/HEAD) Edycja README: architektura, instrukcja uruchomienia i zmienne środowiskowe
5ef09b1 Compose z dwiema sieciami, wolumenem i healthcheckiem
92371e4 Frontend, Streamlit pobiera listę ogłoszeń z backendu
8cf3685 Wzór zmiennych środowiskowych i końce linii LF
e787dd7  endpointy /health i /listings z bazy)
   **Na następne zajęcia:** pokaz KM1, przećwiczenie odpowiedzi na pytania

   ## Zajęcia 3 Wiktor
**Zrobione:** pokaz KM1: 3 kontenery, frontend → backend → baza, izolacja sieci, trwałość danych; pokaz awarii bazy na prośbę prowadzącego
**Ujawnione wymagania backendu:** min. 4 endpointy (GET pojedynczy, GET lista, POST, PUT/PATCH lub DELETE); JSON udokumentowany w README; walidacja (400); 404 dla nieistniejącego zasobu; /health; healthcheck w compose na /health + depends_on: service_healthy; konfiguracja przez zmienne środowiskowe
**Problemy i rozwiązanie:** zatrzymanie bazy dawało 500 na froncie → backend zwraca 503, frontend rozróżnia awarię bazy i backendu
**Na następne zajęcia:** implementacja API


## Zajęcia 4 Wiktor
**Zrobione:** (Wiktor: obsługa błędów 400/503, GET /listings z wyszukiwarką, GET /listings/{id} z 404, POST, GET /categories, pliki JSON do testów | Paweł: healthcheck backendu na /health + depends_on service_healthy, PUT i DELETE z 404)
**Problemy i rozwiązanie:** (np. PowerShell psuł JSON w curl → dane w plikach scripts/*.json)
**Commity:** (git log --oneline -8)
**Na następne zajęcia:** testy API (pytest), dokumentacja API w README, skrypt pokazowy

## Zajęcia 5 Wiktor
**Zrobione:** (Wiktor: testy odczytu test_read.py, skrypt demo.ps1 | Paweł: testy zapisu test_write.py, dokumentacja API w README)
**Problemy i rozwiązanie:** (np. testy wymagają przebudowy obrazu, bo kod jest kopiowany przy buildzie)
**Commity:** (git log --oneline -6)
**Na następne zajęcia:** pokaz KM2