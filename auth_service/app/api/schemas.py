from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType, uuid4
from sqlalchemy import Column, String, Integer, DateTime

class UserSchema(BaseModel):
    id: UUIDType
    username: str
    name: str
    email: str
    status: int
    birthday: Optional[DateTime]
    created_at: DateTime
    team_id: Optional[UUIDType]

    class Config:
        orm_mode = True

class TeamSchema(BaseModel):
    id: UUIDType
    name: str
    created: DateTime

    class Config:
        orm_mode = True
