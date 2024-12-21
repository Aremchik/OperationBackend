from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.api.database.database import Base

# Модель пользователя
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
    
    # Изменим имя свойства связи на 'team_association', чтобы избежать конфликта
    team_id = Column(String, ForeignKey("teams.id"), nullable=True)
    
    # Обратная связь
    team = relationship("TeamModel", backref="members", lazy="dynamic")


# Модель команды
class TeamModel(Base):
    __tablename__ = "teams"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created = Column(DateTime, server_default=func.now(), nullable=False)

    # Связь с участниками
    members = relationship("UserModel", backref="team_association", lazy="dynamic")


# Модель для связей участников команды
class TeamMemberModel(Base):
    __tablename__ = "team_members"

    team_id = Column(String, ForeignKey("teams.id"), primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)

    # Дополнительные связи (если нужны) могут быть добавлены сюда
