$API = "http://localhost:8000"
function Show($title) { Write-Host "`n=== $title ===" -ForegroundColor Cyan }

Show "1. GET /health -> 200"
curl.exe -s -i "$API/health"

Show "2. GET /listings -> 200 (lista)"
curl.exe -s "$API/listings"

Show "3. GET /listings?q=rower&max_price=1000&sort=price_asc -> 200 (wyszukiwarka)"
curl.exe -s "$API/listings?q=rower&max_price=1000&sort=price_asc"

Show "4. GET /listings/2 -> 200 (pojedynczy zasob)"
curl.exe -s -i "$API/listings/2"

Show "5. GET /listings/999999 -> 404"
curl.exe -s -i "$API/listings/999999"

Show "6. GET /listings/abc -> 400 (zly typ id)"
curl.exe -s -i "$API/listings/abc"

Show "7. GET /listings?min_price=500&max_price=100 -> 400"
curl.exe -s -i "$API/listings?min_price=500&max_price=100"

Show "8. POST /listings -> 201"
$created = curl.exe -s -X POST "$API/listings" -H "Content-Type: application/json" --data "@scripts/listing_ok.json" | ConvertFrom-Json
$created
$id = $created.id

Show "9. POST /listings z blednymi danymi -> 400"
curl.exe -s -i -X POST "$API/listings" -H "Content-Type: application/json" --data "@scripts/listing_bad.json"

Show "10. POST /listings z nieistniejaca kategoria -> 400"
curl.exe -s -i -X POST "$API/listings" -H "Content-Type: application/json" --data "@scripts/listing_bad_category.json"

Show "11. PUT /listings/$id -> 200"
curl.exe -s -i -X PUT "$API/listings/$id" -H "Content-Type: application/json" --data "@scripts/listing_update.json"

Show "12. PUT /listings/999999 -> 404"
curl.exe -s -i -X PUT "$API/listings/999999" -H "Content-Type: application/json" --data "@scripts/listing_update.json"

Show "13. DELETE /listings/$id -> 204"
curl.exe -s -i -X DELETE "$API/listings/$id"

Show "14. DELETE /listings/$id ponownie -> 404"
curl.exe -s -i -X DELETE "$API/listings/$id"