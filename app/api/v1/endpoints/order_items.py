from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud.crud_order_item import create_order_item, delete_order_item, get_order_item, list_order_items
from app.schemas.order_item import OrderItemCreate, OrderItemOut

router = APIRouter(prefix="/order-items", tags=["order-items"])


@router.get("", response_model=list[OrderItemOut])
async def read_items(db: AsyncSession = Depends(get_db)):
    return await list_order_items(db)


@router.post("", response_model=OrderItemOut, status_code=status.HTTP_201_CREATED)
async def create_new_item(payload: OrderItemCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_item = await create_order_item(db, payload)
        from app.metrics import TOTAL_REVENUE
        TOTAL_REVENUE.inc(new_item.qty * new_item.unit_price)
        return new_item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_item(item_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_order_item(db, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Order item not found")
    await delete_order_item(db, obj)
    return None