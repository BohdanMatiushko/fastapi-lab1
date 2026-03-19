from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile
from app.schemas.profile import ProfileCreate


async def list_profiles(db: AsyncSession) -> list[Profile]:
    res = await db.execute(select(Profile).order_by(Profile.id))
    return list(res.scalars().all())


async def get_profile(db: AsyncSession, profile_id: int) -> Profile | None:
    return await db.get(Profile, profile_id)


async def create_profile(db: AsyncSession, payload: ProfileCreate) -> Profile:
    obj = Profile(user_id=payload.user_id, full_name=payload.full_name, phone=payload.phone)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_profile(db: AsyncSession, obj: Profile) -> None:
    await db.delete(obj)
    await db.commit()