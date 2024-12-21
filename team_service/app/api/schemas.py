from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TeamSchema(BaseModel):
    id: str
    name: str
    created: datetime
    members: List[str] = []  # Здесь можно использовать пользовательские id или UserSchema, если они доступны.

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    id: str
    username: str
    name: str
    email: str
    password: str
    status: int
    birthday: datetime
    created_at: datetime
    team: Optional[str] = None  # Добавлено поле team с значением None по умолчанию

    class Config:
        orm_mode = True

class CreateTeamSchema(BaseModel):
    name: str
    members: List[str]  # Список usernames участников

    class Config:
        orm_mode = True