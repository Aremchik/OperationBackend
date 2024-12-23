from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers import team
from app.api.database.database import engine, Base
from threading import Thread
from app.api.rabbitmq.consumer import start_consumer

def start_rabbitmq_listener():
    Thread(target=start_consumer, daemon=True).start()

start_rabbitmq_listener()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.
    """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    try:
        yield
    finally:
        pass

app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/v1/team/openapi.json",
    docs_url="/api/v1/team/docs"
)

app.include_router(team.router, prefix="/api/v1/team", tags=["team Service"])
