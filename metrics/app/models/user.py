from sqlalchemy import Column, Integer, String, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums.user_role import UserRole



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, nullable=False, default=UserRole.USER.value)
    __table_args__ = (
    CheckConstraint(
        f"role IN ('{UserRole.ADMIN.value}', '{UserRole.USER.value}')",
        name="check_user_role"
    ),)
    hashed_password = Column(String)

    metrics = relationship("Metric", back_populates="user")
