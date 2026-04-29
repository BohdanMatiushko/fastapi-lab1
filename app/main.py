from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.seed import seed_if_empty
from app.db.session import AsyncSessionLocal

from prometheus_fastapi_instrumentator import Instrumentator


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as db:
        await seed_if_empty(db)
    yield


app = FastAPI(title="FastAPI Lab 4", lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")