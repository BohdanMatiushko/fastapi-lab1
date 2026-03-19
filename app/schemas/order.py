from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class OrderCreate(BaseModel):
    user_id: int
    status: str = "new"


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    status: str