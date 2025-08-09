from pydantic import BaseModel
from datetime import datetime
from app.models.enums.metric_type import MetricType


class MetricBase(BaseModel):
    type: MetricType
    description: str


class MetricCreate(MetricBase):
    pass


class MetricResponse(MetricBase):
    id: int
    timestamp: datetime


    model_config = {
        "from_attributes": True
    }

