from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    id: str
    username: str
    name: str
    email: str
    password: str
    status: int
    birthday: datetime
    created_at: datetime
    team: Optional[str] = None 

    class Config:
        orm_mode = True
