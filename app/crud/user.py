from sqlalchemy import select
from app.models.user import User

async def get_user_by_username(db, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def create_user(db, username, email, password_hash):
    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user