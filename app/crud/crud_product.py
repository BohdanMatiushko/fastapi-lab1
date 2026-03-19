from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate


async def list_products(db: AsyncSession) -> list[Product]:
    res = await db.execute(select(Product).order_by(Product.id))
    return list(res.scalars().all())


async def get_product(db: AsyncSession, product_id: int) -> Product | None:
    return await db.get(Product, product_id)


async def create_product(db: AsyncSession, payload: ProductCreate) -> Product:
    obj = Product(name=payload.name, price=payload.price, category_id=payload.category_id)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_product(db: AsyncSession, obj: Product) -> None:
    await db.delete(obj)
    await db.commit()