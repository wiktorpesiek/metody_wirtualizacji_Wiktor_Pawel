from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID = {"title": "Test rower", "description": "test", "price": 100, "city": "Poznań"}


def test_create_get_update_delete_flow():
    # POST -> 201
    r = client.post("/listings", json=VALID)
    assert r.status_code == 201
    listing_id = r.json()["id"]

    # GET -> 200
    assert client.get(f"/listings/{listing_id}").json()["title"] == "Test rower"

    # PUT -> 200 i zmienione dane
    updated = {**VALID, "title": "Test rower po zmianie", "price": 80}
    r = client.put(f"/listings/{listing_id}", json=updated)
    assert r.status_code == 200
    assert r.json()["title"] == "Test rower po zmianie"
    assert float(r.json()["price"]) == 80

    # DELETE -> 204, potem 404
    assert client.delete(f"/listings/{listing_id}").status_code == 204
    assert client.get(f"/listings/{listing_id}").status_code == 404


def test_negative_price_returns_400():
    r = client.post("/listings", json={**VALID, "price": -5})
    assert r.status_code == 400
    assert any(e["field"] == "price" for e in r.json()["errors"])


def test_too_short_title_returns_400():
    assert client.post("/listings", json={**VALID, "title": "X"}).status_code == 400


def test_missing_price_returns_400():
    data = {k: v for k, v in VALID.items() if k != "price"}
    assert client.post("/listings", json=data).status_code == 400


def test_invalid_json_returns_400():
    r = client.post("/listings", content="to nie jest json", headers={"Content-Type": "application/json"})
    assert r.status_code == 400


def test_nonexistent_category_returns_400():
    r = client.post("/listings", json={**VALID, "category_id": 999999})
    assert r.status_code == 400
    assert r.json()["detail"] == "Kategoria nie istnieje"


def test_put_nonexistent_returns_404():
    assert client.put("/listings/999999", json=VALID).status_code == 404


def test_delete_nonexistent_returns_404():
    assert client.delete("/listings/999999").status_code == 404
