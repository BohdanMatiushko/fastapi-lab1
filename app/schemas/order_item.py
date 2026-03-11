from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    qty: int = Field(ge=1)


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: int
    product_id: int
    qty: int
    unit_price: float