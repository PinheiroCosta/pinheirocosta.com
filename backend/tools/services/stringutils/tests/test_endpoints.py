from fastapi.testclient import TestClient
from app.main import app  # Ajuste o import conforme seu setup

client = TestClient(app)

def test_reverse():
    resp = client.post("/reverse", json={"text": "abc"})
    assert resp.status_code == 200
    assert resp.json() == {"result": "cba"}

def test_uppercase():
    resp = client.post("/uppercase", json={"text": "abc"})
    assert resp.status_code == 200
    assert resp.json() == {"result": "ABC"}

def test_slugify():
    resp = client.post("/slugify", json={"text": "Olá Mundo!"})
    assert resp.status_code == 200
    assert resp.json() == {"result": "ola-mundo"}

def test_uuid():
    resp = client.post("/uuid")
    assert resp.status_code == 200
    assert "result" in resp.json()
    assert len(resp.json()["result"]) == 36

