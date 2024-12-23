from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.database.database import get_db
from app.api.model.model import UserModel
from app.api.schemas import UserSchema
from pydantic import BaseModel
from uuid import UUID
from sqlalchemy import select

router = APIRouter()

@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)) -> UserSchema:
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    result = await db.execute(select(UserModel).where(UserModel.id == user_uuid))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserSchema.from_orm(user)

@router.post("/users/", response_model=UserSchema)
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    user_model = UserModel(**user.dict())
    db.add(user_model)
    await db.commit()
    await db.refresh(user_model)
    return UserSchema.from_orm(user_model)

@router.put("/users/{user_id}", response_model=UserSchema)
async def update_user(user_id: str, user: UserSchema, db: AsyncSession = Depends(get_db)):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    existing_user = await db.get(UserModel, user_uuid)

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict().items():
        setattr(existing_user, key, value)

    await db.commit()
    await db.refresh(existing_user)
    return UserSchema.from_orm(existing_user)

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    user = await db.get(UserModel, user_uuid)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted"}