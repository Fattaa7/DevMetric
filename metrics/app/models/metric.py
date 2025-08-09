from datetime import datetime
from sqlalchemy import CheckConstraint, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums.metric_type import MetricType



class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String, nullable=False, default=MetricType.COMMIT.value)
    __table_args__ = (
    CheckConstraint(
        f"type IN ('{MetricType.COMMIT.value}', '{MetricType.TASK.value}')",
        name="check_metric_type"
    ),)
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="metrics")
