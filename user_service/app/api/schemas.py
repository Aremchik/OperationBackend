from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType, uuid4
from datetime import datetime as DatetimeType
import pytz  # Импортируем pytz для работы с часовыми поясами

class UserSchema(BaseModel):
    id: UUIDType
    username: str
    name: str
    email: str
    status: int
    password: Optional[str]  # Add password here to avoid missing attribute error
    birthday: Optional[datetime]
    created_at: datetime
    team_id: Optional[UUIDType]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def validate_birthday(cls, birthday: Optional[datetime]):
        if birthday is not None:
            # Приводим дату ко всем к одному часовому поясу UTC
            return birthday.astimezone(pytz.UTC)
        return birthday

class TeamSchema(BaseModel):
    id: UUIDType
    name: str
    created: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
