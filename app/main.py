from __future__ import annotations

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.seed import seed_if_empty
from app.db.session import AsyncSessionLocal

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="FastAPI Lab 4")

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.on_event("startup")
async def startup_seed() -> None:
    async with AsyncSessionLocal() as db:
        await seed_if_empty(db)