
import os
from fastapi import FastAPI

from .api.v1 import router as api_v1_router
from .db.pool import init_pool, close_pool

DATABASE_URL = os.getenv("DATABASE_URL")
assert DATABASE_URL is not None, "DATABASE_URL environment variable is not set!"
app = FastAPI()

app.include_router(api_v1_router, prefix="/api/v1")


@app.on_event("startup")
async def startup() -> None:
    await init_pool(DATABASE_URL)


@app.on_event("shutdown")
async def shutdown() -> None:
    await close_pool()
