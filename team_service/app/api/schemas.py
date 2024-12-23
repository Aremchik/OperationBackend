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
    members: List[UserSchema] = [] 

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        from_attributes = True
class CreateTeamSchema(BaseModel):
    name: str
    members: List[str] 

    class Config:
        orm_mode = True