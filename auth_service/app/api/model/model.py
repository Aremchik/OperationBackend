from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUID для id
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Integer, default=1)  # 1 = Active, 0 = Inactive
    birthday = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Ссылка на команду с использованием UUID
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=True)
    
    # Измените это на обычное отношение без lazy="dynamic"
    team = relationship("TeamModel", backref="team_members")





# Модель команды
class TeamModel(Base):
    __tablename__ = "teams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUID для id
    name = Column(String, nullable=False)
    created = Column(DateTime, server_default=func.now(), nullable=False)

    # Связь с пользователями через обратную связь
    members = relationship("UserModel", backref="user_team", lazy="select")




# Модель для связей участников команды
class TeamMemberModel(Base):
    __tablename__ = "team_members"

    team_id = Column(String, ForeignKey("teams.id"), primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)

    # Дополнительные связи (если нужны) могут быть добавлены сюда
