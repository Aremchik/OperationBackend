from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    name: str
    email: str
    password: str
    birthday: str  # Дата рождения
    team_id: Optional[str] = None  # Опциональное поле team_id, по умолчанию None

    class Config:
        orm_mode = True
