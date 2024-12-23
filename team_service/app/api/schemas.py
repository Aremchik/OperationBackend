from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import pytz 
from uuid import UUID as UUIDType, uuid4

class UserSchema(BaseModel):
    id: UUIDType
    username: str
    name: str
    email: str
    password: Optional[str]  # Пароль можно передать при регистрации, но не выводить в ответ
    status: int  # 1 = Active, 0 = Inactive
    birthday: Optional[datetime]
    created_at: datetime
    team_id: Optional[UUIDType]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        from_attributes = True  # Эта строка необходима для метода from_orm

    @classmethod
    def validate_birthday(cls, birthday: Optional[datetime]):
        if birthday is not None:
            # Приводим дату к часовому поясу UTC
            return birthday.astimezone(pytz.UTC)
        return birthday

class TeamSchema(BaseModel):
    id: UUIDType
    name: str
    created: datetime
    members: List[UserSchema] = []  # Здесь добавляем список участников команды

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        from_attributes = True

class CreateTeamSchema(BaseModel):
    name: str
    members: List[str]  # Список usernames участников

    class Config:
        orm_mode = True