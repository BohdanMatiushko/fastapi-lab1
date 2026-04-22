import pytest
from app.crud.crud_user import create_user, get_user, list_users, update_user, delete_user
from app.schemas.user import UserCreate, UserUpdate

@pytest.mark.asyncio
async def test_create_user(db_session):
    payload = UserCreate(email="test1@test.com", username="user1")
    user = await create_user(db_session, payload)
    assert user.id is not None
    assert user.email == "test1@test.com"
    assert user.username == "user1"

@pytest.mark.asyncio
async def test_get_user(db_session):
    payload = UserCreate(email="test2@test.com", username="user2")
    created = await create_user(db_session, payload)
    
    fetched = await get_user(db_session, created.id)
    assert fetched is not None
    assert fetched.email == "test2@test.com"

@pytest.mark.asyncio
async def test_list_users(db_session):
    users = await list_users(db_session)
    assert isinstance(users, list)

@pytest.mark.asyncio
async def test_update_user(db_session):
    user = await create_user(db_session, UserCreate(email="test3@test.com", username="user3"))
    
    updated = await update_user(db_session, user, UserUpdate(username="new_user3"))
    assert updated.username == "new_user3"

@pytest.mark.asyncio
async def test_delete_user(db_session):
    user = await create_user(db_session, UserCreate(email="delete@test.com", username="delete"))
    await delete_user(db_session, user)
    
    fetched = await get_user(db_session, user.id)
    assert fetched is None
