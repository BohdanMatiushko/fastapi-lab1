from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud.crud_user import create_user, delete_user, get_user, list_users, update_user
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def read_users_me(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id}


@router.get("", response_model=list[UserOut])
@router.get("/", response_model=list[UserOut], include_in_schema=False)
async def read_users(db: AsyncSession = Depends(get_db)):
    return await list_users(db)


@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_new_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, payload)


@router.put("/{user_id}", response_model=UserOut)
async def update_existing_user(user_id: int, payload: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await update_user(db, user, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await delete_user(db, user)
    return None