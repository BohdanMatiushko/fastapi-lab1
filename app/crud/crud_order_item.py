from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order_item import OrderItemCreate


async def list_order_items(db: AsyncSession) -> list[OrderItem]:
    res = await db.execute(select(OrderItem).order_by(OrderItem.id))
    return list(res.scalars().all())


async def get_order_item(db: AsyncSession, item_id: int) -> OrderItem | None:
    return await db.get(OrderItem, item_id)


async def create_order_item(db: AsyncSession, payload: OrderItemCreate) -> OrderItem:
    product = await db.get(Product, payload.product_id)
    if product is None:
        raise ValueError("Product not found")

    obj = OrderItem(
        order_id=payload.order_id,
        product_id=payload.product_id,
        qty=payload.qty,
        unit_price=float(product.price),
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_order_item(db: AsyncSession, obj: OrderItem) -> None:
    await db.delete(obj)
    await db.commit()