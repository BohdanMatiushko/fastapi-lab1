from __future__ import annotations

from typing import List

from fastapi import HTTPException, status

from app.db.mem_db import db
from app.schemas.user import UserCreate, UserUpdate


def list_users() -> List[dict]:
    with db.lock:
        return [db.users[user_id] for user_id in sorted(db.users.keys())]


def get_user(user_id: int) -> dict:
    with db.lock:
        user = db.users.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user


def create_user(payload: UserCreate) -> dict:
    with db.lock:
        user_id = db.next_id
        db.next_id += 1

        user = {
            "id": user_id,
            "username": payload.username,
            "email": str(payload.email),
            "is_active": payload.is_active,
        }
        db.users[user_id] = user
        return user


def update_user(user_id: int, payload: UserUpdate) -> dict:
    with db.lock:
        user = db.users.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        data = payload.model_dump(exclude_unset=True)

        if "username" in data and data["username"] is not None:
            user["username"] = data["username"]
        if "email" in data and data["email"] is not None:
            user["email"] = str(data["email"])
        if "is_active" in data and data["is_active"] is not None:
            user["is_active"] = data["is_active"]

        db.users[user_id] = user
        return user


def delete_user(user_id: int) -> None:
    with db.lock:
        if user_id not in db.users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        del db.users[user_id]