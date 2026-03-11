from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.schemas.order import OrderCreate


async def list_orders(db: AsyncSession) -> list[Order]:
    res = await db.execute(select(Order).order_by(Order.id))
    return list(res.scalars().all())


async def get_order(db: AsyncSession, order_id: int) -> Order | None:
    return await db.get(Order, order_id)


async def create_order(db: AsyncSession, payload: OrderCreate) -> Order:
    obj = Order(user_id=payload.user_id, status=payload.status)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_order(db: AsyncSession, obj: Order) -> None:
    await db.delete(obj)
    await db.commit()