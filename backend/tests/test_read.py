from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_returns_json_list():
    r = client.get("/listings")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1


def test_search_by_phrase():
    r = client.get("/listings", params={"q": "rower"})
    assert r.status_code == 200
    results = r.json()
    assert len(results) >= 1
    assert all("rower" in (x["title"] + x["description"]).lower() for x in results)


def test_price_filter_and_sort():
    r = client.get("/listings", params={"max_price": 1000, "sort": "price_asc"})
    assert r.status_code == 200
    prices = [float(x["price"]) for x in r.json()]
    assert all(p <= 1000 for p in prices)
    assert prices == sorted(prices)


def test_min_price_greater_than_max_returns_400():
    r = client.get("/listings", params={"min_price": 500, "max_price": 100})
    assert r.status_code == 400


def test_invalid_query_param_returns_400():
    assert client.get("/listings", params={"min_price": "abc"}).status_code == 400


def test_get_single_listing():
    first_id = client.get("/listings").json()[0]["id"]
    r = client.get(f"/listings/{first_id}")
    assert r.status_code == 200
    assert r.json()["id"] == first_id


def test_get_nonexistent_listing_returns_404():
    r = client.get("/listings/999999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Ogłoszenie nie istnieje"


def test_get_listing_with_invalid_id_returns_400():
    assert client.get("/listings/abc").status_code == 400


def test_sql_injection_is_treated_as_text():
    r = client.get("/listings", params={"q": "' OR 1=1 --"})
    assert r.status_code == 200
    assert r.json() == []


def test_categories():
    r = client.get("/categories")
    assert r.status_code == 200
    assert {"id", "name"} <= set(r.json()[0])