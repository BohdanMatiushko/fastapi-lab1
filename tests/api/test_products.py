import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_product_api(async_client: AsyncClient):
    # Спочатку створюємо категорію
    cat_payload = {"name": "Test Cat for Prod"}
    cat_res = await async_client.post("/api/v1/categories", json=cat_payload)
    cat_id = cat_res.json()["id"]

    prod_payload = {
        "name": "API Laptop",
        "price": 1500.0,
        "category_id": cat_id
    }
    response = await async_client.post("/api/v1/products", json=prod_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "API Laptop"
    assert data["price"] == 1500.0
    assert "id" in data

@pytest.mark.asyncio
async def test_list_products_api(async_client: AsyncClient):
    response = await async_client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_delete_product_api(async_client: AsyncClient):
    # Створюємо категорію
    cat_payload = {"name": "Test Cat for Prod 2"}
    cat_res = await async_client.post("/api/v1/categories", json=cat_payload)
    cat_id = cat_res.json()["id"]

    # Створюємо продукт
    prod_payload = {"name": "To Delete", "price": 10.0, "category_id": cat_id}
    res = await async_client.post("/api/v1/products", json=prod_payload)
    created = res.json()
    
    del_res = await async_client.delete(f"/api/v1/products/{created['id']}")
    assert del_res.status_code == 204
