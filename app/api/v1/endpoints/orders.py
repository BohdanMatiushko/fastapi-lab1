from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud.crud_order import create_order, delete_order, get_order, list_orders
from app.schemas.order import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderOut])
async def read_orders(db: AsyncSession = Depends(get_db)):
    return await list_orders(db)


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_new_order(payload: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await create_order(db, payload)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_order(order_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_order(db, order_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Order not found")
    await delete_order(db, obj)
    return None