from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "The Foo ID",
        "description": "The Foo description",
    }


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_nonexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foobar",
            "title": "The Foo Bar",
            "description": "The Foo Bar description",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "The Foo Bar",
        "description": "The Foo Bar description",
    }


def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={
            "id": "foobar",
            "title": "The Foo Bar",
            "description": "The Foo Bar description",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foobar",
            "title": "The Foo Bar",
            "description": "The Foo Bar description",
        },
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}
