from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.api.database.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Integer, default=1)  # 1 = Active, 0 = Inactive
    birthday = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Поле team с ForeignKey
    team = Column(String, ForeignKey("teams.id"), nullable=True)
    
    # Связь с TeamModel
    team_relation = relationship("TeamModel", back_populates="users")



class TeamModel(Base):
    __tablename__ = "teams"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    created = Column(DateTime, server_default=func.now(), nullable=False)

    # Связь с UserModel
    users = relationship("UserModel", back_populates="team_relation")


class TeamMembers(Base):
    __tablename__ = "team_members"

    team_id = Column(String, ForeignKey('teams.id'), primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), primary_key=True)
