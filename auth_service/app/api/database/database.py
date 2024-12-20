# Убедитесь, что SQLAlchemy версии 1.4 или выше
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import asyncio

DATABASE_URL = "sqlite+aiosqlite:///D:/prod/Prilo/Labs/kursach/operation.sqlite"

Base = declarative_base()

# Используйте create_async_engine для асинхронных операций
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session

# Функция для создания таблиц
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Запускаем функцию инициализации базы данных
asyncio.run(init_db())