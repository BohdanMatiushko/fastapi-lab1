from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import CategoryCreate


async def list_categories(db: AsyncSession) -> list[Category]:
    res = await db.execute(select(Category).order_by(Category.id))
    return list(res.scalars().all())


async def get_category(db: AsyncSession, category_id: int) -> Category | None:
    return await db.get(Category, category_id)


async def create_category(db: AsyncSession, payload: CategoryCreate) -> Category:
    obj = Category(name=payload.name)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_category(db: AsyncSession, obj: Category) -> None:
    await db.delete(obj)
    await db.commit()