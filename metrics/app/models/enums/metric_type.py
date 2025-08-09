from enum import Enum

class MetricType(str, Enum):
    COMMIT = "commit"
    TASK = "task"
