from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api import router as api_router
from src.config import settings
from src.database.database_helper import db_helper
from src.models import Base
from src.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Для создания таблиц в БД
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    await redis_client.connect()
    yield
    await redis_client.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=settings.port, reload=True)
