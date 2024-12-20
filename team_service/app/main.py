from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routers import team
from api.database.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.
    """
    async with engine.begin() as connection:
        # Убедитесь, что таблицы создаются только один раз
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
