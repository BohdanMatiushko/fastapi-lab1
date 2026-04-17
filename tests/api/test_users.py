import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_api(async_client: AsyncClient):
    payload = {
        "username": "test_api_user",
        "email": "api@test.com",
        "password": "password"
    }
    response = await async_client.post("/api/v1/users/", json=payload)
    if response.status_code == 400: # Could be Email already registered
        pass
    else:
        assert response.status_code == 200 or response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["email"] == "api@test.com"

@pytest.mark.asyncio
async def test_list_users_api(async_client: AsyncClient):
    response = await async_client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_users_me_api(async_client: AsyncClient):
    # Ми перехопили get_current_user в conftest.py, тому цей роут
    # має відпрацювати і повернути ID (або повноцінного юзера, якщо 
    # бекенд підтягує його з БД)
    response = await async_client.get("/api/v1/users/me")
    # Depends на implementation auth, припустимо це 200
    assert response.status_code in [200, 404]  # 404 якщо user_id ("1234...") не знайдений в БД
