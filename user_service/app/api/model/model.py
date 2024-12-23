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
    status = Column(Integer, default=1)  # 1 = Active, 0 = Inactive
    birthday = Column(DateTime(timezone=True), nullable=True)  # Дата с часовым поясом
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Дата с часовым поясом
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    team = relationship("TeamModel", back_populates="members")
