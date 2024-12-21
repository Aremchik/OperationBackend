from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.database.database import get_db
from sqlalchemy.future import select
from app.api.model.model import UserModel, TeamModel  # Импортируем новые модели
from app.api.schemas import UserSchema
from app.api.utils.jwt import create_access_token, verify_token
from pydantic import BaseModel
from passlib.context import CryptContext
from uuid import uuid4
from datetime import datetime

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Класс для создания пользователя
class UserCreate(BaseModel):
    username: str
    name: str
    email: str
    password: str
    birthday: str  # Оставляем дату как строку, которую будем конвертировать
    team_id: str  # Новый параметр для привязки пользователя к команде

# Класс для аутентификации (логин)
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(UserModel).where(UserModel.username == username))
    return result.scalar_one_or_none()

async def get_team(db: AsyncSession, team_id: str):
    result = await db.execute(select(TeamModel).where(TeamModel.id == team_id))
    return result.scalar_one_or_none()

@router.post("/register", response_model=UserSchema)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    # Преобразуем строку с датой в объект datetime
    birthday = datetime.fromisoformat(user.birthday[:-1])  # Удаляем 'Z'

    hashed_password = pwd_context.hash(user.password)

    new_user = UserModel(
        id=str(uuid4()),  # Генерация уникального идентификатора
        username=user.username,
        name=user.name,
        email=user.email,
        password=hashed_password,
        birthday=birthday,  # Добавляем дату рождения
        team_id=user.team_id,  # Устанавливаем team_id, которое может быть None
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user



@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user(db, user.username)
    if not existing_user or not pwd_context.verify(user.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # Создаем токен для пользователя
    access_token = create_access_token(data={"sub": existing_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserSchema)
async def read_users_me(token: str, db: AsyncSession = Depends(get_db)):
    user_payload = verify_token(token)
    if user_payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    username = user_payload.get("sub")
    user = await get_user(db, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
