from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers import user
from app.api.database.database import engine, Base  
import threading
from app.api.rabbitmq.consumer import start_consuming

def start_rabbitmq_listener():
    threading.Thread(target=start_consuming, daemon=True).start()


start_rabbitmq_listener()

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        
    try:
        yield
    finally:
        pass

app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/v1/user/openapi.json",
    docs_url="/api/v1/user/docs"
)

app.include_router(user.router, prefix="/api/v1/user", tags=["User Service"])

