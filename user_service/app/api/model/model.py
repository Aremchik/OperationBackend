from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, select
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.api.database.database import Base
from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID as UUIDType, uuid4

class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Integer, default=1)  
    birthday = Column(DateTime(timezone=True), nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    team = relationship("TeamModel", back_populates="members")

class TeamModel(Base):
    __tablename__ = "teams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 
    members = relationship("UserModel", back_populates="team")

class TeamMemberModel(Base):
    __tablename__ = "team_members"

    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)