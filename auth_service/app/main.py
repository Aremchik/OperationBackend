from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers import auth_router
from app.api.database.database import engine, Base

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
    openapi_url="/api/v1/auth/openapi.json",
    docs_url="/api/v1/auth/docs"
)

app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Auth Service"])
