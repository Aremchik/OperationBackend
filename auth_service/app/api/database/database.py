from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Измените URL базы данных на PostgreSQL
DATABASE_URL = "postgresql+asyncpg://postgres:password@postgres:5432/postgres"

Base = declarative_base()

# Создаем движок и сессию для работы с базой данных
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session

# Функция для инициализации базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
