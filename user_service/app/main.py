from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routers import user
from api.database.database import engine, Base  # Убедитесь, что вы импортировали правильные объекты
import threading
from api.rabbitmq.consumer import start_consuming

def start_rabbitmq_listener():
    threading.Thread(target=start_consuming, daemon=True).start()

# Запускаем listener при старте приложения
start_rabbitmq_listener()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.
    Выполняет подключение к базе данных при запуске приложения
    и разрывает соединение при его остановке.
    """
    # Создание таблиц в базе данных на старте
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        
    try:
        yield
    finally:
        # Убедитесь, что никаких дополнительных действий не требуется здесь
        pass

app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/v1/user/openapi.json",
    docs_url="/api/v1/user/docs"
)

app.include_router(user.router, prefix="/api/v1/user", tags=["User Service"])

