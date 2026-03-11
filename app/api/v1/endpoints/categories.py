from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud.crud_category import create_category, delete_category, get_category, list_categories
from app.schemas.category import CategoryCreate, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
async def read_categories(db: AsyncSession = Depends(get_db)):
    return await list_categories(db)


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_new_category(payload: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await create_category(db, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_category(category_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_category(db, category_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    await delete_category(db, obj)
    return None