from __future__ import annotations

from typing import List

from fastapi import APIRouter, status

from app.crud.crud_user_mem import (
    create_user,
    delete_user,
    get_user,
    list_users,
    update_user,
)
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserOut])
def read_users() -> List[UserOut]:
    return list_users()


@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int) -> UserOut:
    return get_user(user_id)


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_new_user(payload: UserCreate) -> UserOut:
    return create_user(payload)


@router.put("/{user_id}", response_model=UserOut)
def update_existing_user(user_id: int, payload: UserUpdate) -> UserOut:
    return update_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_user(user_id: int) -> None:
    delete_user(user_id)
    return None