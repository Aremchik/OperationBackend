from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.database.database import get_db
from app.api.model.model import UserModel
from app.api.schemas import UserSchema
from pydantic import BaseModel
from uuid import UUID
from sqlalchemy import select

router = APIRouter()

# Получение пользователя
@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(db: AsyncSession, user_id: str) -> UserSchema:
    try:
        # Приведение user_id к UUID
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    result = await db.execute(select(UserModel).where(UserModel.id == user_uuid))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# Создание нового пользователя
@router.post("/users/", response_model=UserSchema)
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    user_model = UserModel(**user.dict())
    db.add(user_model)
    await db.commit()
    await db.refresh(user_model)
    return user_model

# Обновление информации о пользователе
@router.put("/users/{user_id}", response_model=UserSchema)
async def update_user(user_id: str, user: UserSchema, db: AsyncSession = Depends(get_db)):
    existing_user = await db.get(UserModel, user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict().items():
        setattr(existing_user, key, value)

    await db.commit()
    await db.refresh(existing_user)
    return existing_user

# Удаление пользователя
@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await db.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted"}
