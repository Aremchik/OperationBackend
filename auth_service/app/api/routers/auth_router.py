from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.database.database import get_db
from app.api.schemas import UserSchema, TeamSchema
from app.api.model.model import UserModel
from app.api.utils.jwt import create_access_token, verify_token
from passlib.context import CryptContext
from uuid import UUID
from datetime import datetime as DatetimeType
from pydantic import BaseModel
from app.api.rabbitmq.producer import publish_message

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserSchema)
async def register(user: UserSchema, db: AsyncSession = Depends(get_db)):

    user.birthday = user.validate_birthday(user.birthday)
    
    existing_user = await db.execute(
        select(UserModel).where(UserModel.username == user.username)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    hashed_password = pwd_context.hash(user.password)
    new_user = UserModel(
        id=user.id,
        username=user.username,
        name=user.name,
        email=user.email,
        password=hashed_password,
        birthday=user.birthday,
        team_id=None, 
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    publish_message(
        exchange="user_exchange",
        routing_key="user.registered",
        message={"username": user.username, "email": user.email, "action": "User Registered"}
    )
    return new_user

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(
        select(UserModel).where(UserModel.username == user.username)
    )
    user_instance = existing_user.scalar_one_or_none()
    if not user_instance or not pwd_context.verify(user.password, user_instance.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user_instance.username})
    return {"access_token": access_token, "token_type": "bearer"}