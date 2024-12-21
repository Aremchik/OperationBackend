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

class UserCreate(BaseModel):
    username: str
    name: str
    email: str
    password: str
    birthday: str  # Дата рождения
    team_id: Optional[str] = None  # Опциональное поле team_id, по умолчанию None

    class Config:
        orm_mode = True


class CreateTeamSchema(BaseModel):
    name: str
    members: List[str]  # Список usernames участников

    class Config:
        orm_mode = True