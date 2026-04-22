import pytest
from app.crud.crud_order import create_order, get_order, list_orders, delete_order
from app.crud.crud_user import create_user
from app.schemas.order import OrderCreate
from app.schemas.user import UserCreate

@pytest.mark.asyncio
async def test_create_order(db_session):
    # Створюємо юзера
    user_payload = UserCreate(email="order@test.com", username="order_user")
    user = await create_user(db_session, user_payload)

    # Замовлення
    payload = OrderCreate(user_id=user.id, status="pending")
    order = await create_order(db_session, payload)
    assert order.id is not None
    assert order.status == "pending"

@pytest.mark.asyncio
async def test_get_order(db_session):
    user_payload = UserCreate(email="get_order@test.com", username="get_order")
    user = await create_user(db_session, user_payload)

    payload = OrderCreate(user_id=user.id, status="completed")
    order = await create_order(db_session, payload)

    fetched = await get_order(db_session, order.id)
    assert fetched is not None
    assert fetched.status == "completed"

@pytest.mark.asyncio
async def test_list_orders(db_session):
    orders = await list_orders(db_session)
    assert isinstance(orders, list)

@pytest.mark.asyncio
async def test_delete_order(db_session):
    user_payload = UserCreate(email="del_order@test.com", username="del_order")
    user = await create_user(db_session, user_payload)

    order = await create_order(db_session, OrderCreate(user_id=user.id, status="pending"))
    await delete_order(db_session, order)
    
    fetched = await get_order(db_session, order.id)
    assert fetched is None
