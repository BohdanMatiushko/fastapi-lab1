from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud.crud_profile import create_profile, delete_profile, get_profile, list_profiles
from app.schemas.profile import ProfileCreate, ProfileOut

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("", response_model=list[ProfileOut])
async def read_profiles(db: AsyncSession = Depends(get_db)):
    return await list_profiles(db)


@router.post("", response_model=ProfileOut, status_code=status.HTTP_201_CREATED)
async def create_new_profile(payload: ProfileCreate, db: AsyncSession = Depends(get_db)):
    return await create_profile(db, payload)


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_profile(db, profile_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Profile not found")
    await delete_profile(db, obj)
    return None