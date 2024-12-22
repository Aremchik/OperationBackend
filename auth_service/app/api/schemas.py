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
    birthday: Optional[datetime]
    created_at: datetime
    team_id: Optional[UUIDType]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class TeamSchema(BaseModel):
    id: UUIDType
    name: str
    created: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
