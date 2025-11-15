from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from typing import Annotated

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Items!", "params": commons}


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Users!", "params": commons}


async def override_dependency(q: str | None = None):
    return {"q": q, "skip": 5, "limit": 10}


client = TestClient(app)

app.dependency_overrides[common_parameters] = override_dependency


def test_override_in_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }


def test_override_in_items_with_q():
    response = client.get("/items/", params={"q": "test"})

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "test", "skip": 5, "limit": 10},
    }


def test_override_in_items_with_params():
    response = client.get("/items/", params={"q": "test", "skip": 10, "limit": 20})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "test", "skip": 5, "limit": 10},
    }


def test_no_override_in_items_with_params():
    app.dependency_overrides.clear()
    response = client.get("/items/", params={"q": "test", "skip": 10, "limit": 20})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "test", "skip": 10, "limit": 20},
    }
