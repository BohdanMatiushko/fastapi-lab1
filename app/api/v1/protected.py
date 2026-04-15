from fastapi import APIRouter, Depends
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/me")
async def get_me(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id}

@router.get("/secret")
async def secret(user_id: str = Depends(get_current_user)):
    return {"msg": "you are authenticated"}