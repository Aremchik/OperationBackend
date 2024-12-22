from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType, uuid4
from datetime import datetime as DatetimeType

class UserSchema(BaseModel):
    id: UUIDType
    username: str
    name: str
    email: str
    status: int
    birthday: Optional[DatetimeType]
    created_at: DatetimeType
    team_id: Optional[UUIDType]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class TeamSchema(BaseModel):
    id: UUIDType
    name: str
    created: DatetimeType

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
