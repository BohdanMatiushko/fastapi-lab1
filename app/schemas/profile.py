from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ProfileCreate(BaseModel):
    user_id: int
    full_name: str = Field(min_length=1)
    phone: str | None = None


class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    full_name: str
    phone: str | None