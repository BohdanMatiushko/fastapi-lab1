import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_category_api(async_client: AsyncClient):
    payload = {"name": "Test Cat API"}
    response = await async_client.post("/api/v1/categories", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Cat API"
    assert "id" in data

@pytest.mark.asyncio
async def test_list_categories_api(async_client: AsyncClient):
    payload = {"name": "Test Cat API 2"}
    await async_client.post("/api/v1/categories", json=payload)
    
    response = await async_client.get("/api/v1/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

@pytest.mark.asyncio
async def test_delete_category_api(async_client: AsyncClient):
    payload = {"name": "Delete API"}
    res = await async_client.post("/api/v1/categories", json=payload)
    created = res.json()
    
    del_res = await async_client.delete(f"/api/v1/categories/{created['id']}")
    assert del_res.status_code == 204
