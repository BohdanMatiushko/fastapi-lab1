from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.schemas.auth import RegisterRequest, LoginRequest
from app.crud.user import get_user_by_username, create_user
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# РЕЄСТРАЦІЯ
@router.post("/register")
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, data.username)
    if user:
        raise HTTPException(status_code=400, detail="User exists")

    password_hash = hash_password(data.password)

    user = await create_user(
        db,
        username=data.username,
        email=data.email,
        password_hash=password_hash
    )

    return {"msg": "created"}

# ЛОГІН
@router.post("/login")
async def login(data: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, data.username)

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True
    )

    return {"msg": "logged in"}