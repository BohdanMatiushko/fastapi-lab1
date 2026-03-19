from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud.crud_product import create_product, delete_product, get_product, list_products
from app.schemas.product import ProductCreate, ProductOut

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
async def read_products(db: AsyncSession = Depends(get_db)):
    return await list_products(db)


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_new_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_product(product_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_product(db, product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    await delete_product(db, obj)
    return None