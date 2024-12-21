from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
import uuid
from datetime import datetime
from app.api.database.database import Base

# Модель пользователя
class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    status = Column(Integer)
    birthday = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    team_id = Column(UUID, ForeignKey('teams.id'))  # ссылка на команду
    
    team = relationship("TeamModel", back_populates="members_list")  # связь с командой



# Модель команды
class TeamModel(Base):
    __tablename__ = "teams"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    created = Column(TIMESTAMP, default=datetime.utcnow)

    members_list = relationship("UserModel", back_populates="team")  # связь с пользователями



# Модель для связей участников команды
class TeamMemberModel(Base):
    __tablename__ = "team_members"

    team_id = Column(String, ForeignKey("teams.id"), primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)

    # Дополнительные связи (если нужны) могут быть добавлены сюда
