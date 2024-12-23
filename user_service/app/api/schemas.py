from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType, uuid4
from datetime import datetime as DatetimeType
import pytz  

class UserSchema(BaseModel):
    id: UUIDType
    username: str
    name: str
    email: str
    password: Optional[str] 
    status: int  
    birthday: Optional[datetime]
    created_at: datetime
    team_id: Optional[UUIDType]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        from_attributes = True  

    @classmethod
    def validate_birthday(cls, birthday: Optional[datetime]):
        if birthday is not None:
            return birthday.astimezone(pytz.UTC)
        return birthday

class TeamSchema(BaseModel):
    id: UUIDType
    name: str
    created: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        from_attributes = True  
