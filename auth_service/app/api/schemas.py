from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    username: str
    name: str
    email: str
    password: str
    birthday: str  # Оставляем дату как строку, которую будем конвертировать
    team_id: Optional[str] = None  # Сделать team_id опциональным, чтобы оно было None по умолчанию


    class Config:
        orm_mode = True
