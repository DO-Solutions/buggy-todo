from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_todo():
    r = client.post("/todos", json={"title": "buy milk", "done": True})
    assert r.status_code == 200
    body = r.json()
    assert body["title"] == "buy milk"
    assert body["done"] is True


def test_list_todos():
    client.post("/todos", json={"title": "task a"})
    r = client.get("/todos")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1


def test_get_todo():
    created = client.post("/todos", json={"title": "task b"}).json()
    r = client.get(f"/todos/{created['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]


def test_get_todo_not_found():
    r = client.get("/todos/999999")
    assert r.status_code == 404


def test_delete_todo():
    created = client.post("/todos", json={"title": "task c"}).json()
    r = client.delete(f"/todos/{created['id']}")
    assert r.status_code == 200

    ids = [t["id"] for t in client.get("/todos").json()]
    assert created["id"] not in ids
