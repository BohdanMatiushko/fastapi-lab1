from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def list_users(db: AsyncSession) -> list[User]:
    res = await db.execute(select(User).order_by(User.id))
    return list(res.scalars().all())


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)


async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    user = User(
        username=payload.username,
        email=str(payload.email),
        is_active=payload.is_active,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user: User, payload: UserUpdate) -> User:
    data = payload.model_dump(exclude_unset=True)

    if "username" in data and data["username"] is not None:
        user.username = data["username"]
    if "email" in data and data["email"] is not None:
        user.email = str(data["email"])
    if "is_active" in data and data["is_active"] is not None:
        user.is_active = data["is_active"]

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()