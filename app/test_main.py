from .main import app
from httpx import AsyncClient, ASGITransport
import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}


client = TestClient(app)


@pytest.mark.asyncio
async def test_root_testclient():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
