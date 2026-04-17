import pytest
from httpx import AsyncClient
from app.schemas.order import OrderCreate

@pytest.mark.asyncio
async def test_create_order_api(async_client: AsyncClient):
    # Спочатку створити юзера бо є зовнішній ключ
    user_res = await async_client.post("/api/v1/users/", json={
        "username": "api_order_user",
        "email": "api_order@test.com",
        "password": "pwd"
    })
    user_id = user_res.json()["id"]

    payload = {"user_id": user_id, "status": "pending"}
    response = await async_client.post("/api/v1/orders", json=payload)
    assert response.status_code == 201
    assert response.json()["user_id"] == user_id
    assert response.json()["status"] == "pending"

@pytest.mark.asyncio
async def test_list_orders_api(async_client: AsyncClient):
    response = await async_client.get("/api/v1/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_delete_order_api(async_client: AsyncClient):
    user_res = await async_client.post("/api/v1/users/", json={
        "username": "api_del_order",
        "email": "api_del_order@test.com",
        "password": "pwd"
    })
    
    # Може бути 400 якщо юзер вже існує, але ми робимо кожен раз нового
    user_id = user_res.json()["id"]
    order_res = await async_client.post("/api/v1/orders", json={"user_id": user_id, "status": "pending"})
    order_id = order_res.json()["id"]

    del_res = await async_client.delete(f"/api/v1/orders/{order_id}")
    assert del_res.status_code == 204
