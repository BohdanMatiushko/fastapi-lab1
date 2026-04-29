import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.main import app
from app.core.config import settings
from app.api.deps import get_db, get_current_user
from app.db.base import Base

@pytest_asyncio.fixture(scope="session")
async def engine():
    _engine = create_async_engine(settings.TEST_DATABASE_URL, echo=False, future=True, poolclass=NullPool)
    yield _engine
    await _engine.dispose()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session(engine) -> AsyncSession:
    TestingSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def async_client(db_session: AsyncSession) -> AsyncClient:
    async def override_get_db():
        yield db_session

    def override_get_current_user():
        # Mock user ID for auth testing
        return "12345678-1234-5678-1234-567812345678"

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
