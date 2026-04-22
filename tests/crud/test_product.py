import pytest
from app.crud.crud_product import create_product, list_products, get_product, delete_product
from app.crud.crud_category import create_category
from app.schemas.product import ProductCreate
from app.schemas.category import CategoryCreate

@pytest.mark.asyncio
async def test_create_product(db_session):
    cat_payload = CategoryCreate(name="Electronic")
    category = await create_category(db_session, cat_payload)
    
    prod_payload = ProductCreate(name="Laptop", price=1000.50, category_id=category.id)
    product = await create_product(db_session, prod_payload)
    assert product.id is not None
    assert product.name == "Laptop"
    assert product.category_id == category.id

@pytest.mark.asyncio
async def test_get_product(db_session):
    cat_payload = CategoryCreate(name="Books")
    category = await create_category(db_session, cat_payload)
    
    prod_payload = ProductCreate(name="Book1", price=10.0, category_id=category.id)
    product = await create_product(db_session, prod_payload)
    
    fetched = await get_product(db_session, product.id)
    assert fetched is not None
    assert fetched.name == "Book1"
