import pytest
from app.crud.crud_profile import create_profile, get_profile, list_profiles, delete_profile
from app.crud.crud_user import create_user
from app.schemas.profile import ProfileCreate
from app.schemas.user import UserCreate

@pytest.mark.asyncio
async def test_create_profile(db_session):
    user = await create_user(db_session, UserCreate(email="prof@test.com", username="prof"))
    
    payload = ProfileCreate(user_id=user.id, full_name="John Doe", phone="+123456789")
    profile = await create_profile(db_session, payload)
    
    assert profile.id is not None
    assert profile.full_name == "John Doe"

@pytest.mark.asyncio
async def test_get_profile(db_session):
    user = await create_user(db_session, UserCreate(email="get_prof@test.com", username="get_p"))
    created = await create_profile(db_session, ProfileCreate(user_id=user.id, full_name="Jane", phone="000"))
    
    fetched = await get_profile(db_session, created.id)
    assert fetched is not None
    assert fetched.full_name == "Jane"

@pytest.mark.asyncio
async def test_list_profiles(db_session):
    res = await list_profiles(db_session)
    assert isinstance(res, list)

@pytest.mark.asyncio
async def test_delete_profile(db_session):
    user = await create_user(db_session, UserCreate(email="del_p@test.com", username="dp"))
    profile = await create_profile(db_session, ProfileCreate(user_id=user.id, full_name="To Del", phone="1"))
    
    await delete_profile(db_session, profile)
    
    fetched = await get_profile(db_session, profile.id)
    assert fetched is None
