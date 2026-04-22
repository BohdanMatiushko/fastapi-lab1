import pytest
from app.crud.crud_category import create_category, list_categories, get_category, delete_category
from app.schemas.category import CategoryCreate

@pytest.mark.asyncio
async def test_create_category(db_session):
    payload = CategoryCreate(name="Test Category")
    category = await create_category(db_session, payload)
    assert category.id is not None
    assert category.name == "Test Category"

@pytest.mark.asyncio
async def test_get_category(db_session):
    payload = CategoryCreate(name="Get Category")
    created = await create_category(db_session, payload)
    
    fetched = await get_category(db_session, created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.name == "Get Category"

@pytest.mark.asyncio
async def test_list_categories(db_session):
    payload1 = CategoryCreate(name="Cat 1")
    payload2 = CategoryCreate(name="Cat 2")
    await create_category(db_session, payload1)
    await create_category(db_session, payload2)
    
    categories = await list_categories(db_session)
    assert len(categories) >= 2
    names = [c.name for c in categories]
    assert "Cat 1" in names
    assert "Cat 2" in names

@pytest.mark.asyncio
async def test_delete_category(db_session):
    payload = CategoryCreate(name="Delete Me")
    category = await create_category(db_session, payload)
    
    await delete_category(db_session, category)
    
    fetched = await get_category(db_session, category.id)
    assert fetched is None
