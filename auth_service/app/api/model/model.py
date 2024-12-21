from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.api.database.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Integer, default=1)  # 1 = Active, 0 = Inactive
    birthday = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    team = Column(String, ForeignKey("teams.id"), nullable=True)

# Модель для команд
class TeamModel(Base):
    __tablename__ = "teams"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created = Column(DateTime, server_default=func.now(), nullable=False)

    members = relationship("UserModel", backref="team")

# Модель для связей участников команды
class TeamMemberModel(Base):
    __tablename__ = "team_members"

    team_id = Column(String, ForeignKey("teams.id"), primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
