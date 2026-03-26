from enum import Enum
from pydantic import BaseModel, UUID4, AnyHttpUrl
from typing import Optional


# Описываем все возможные статусы нашей задачи
class TaskStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskResponse(BaseModel):
    task_id: UUID4
    status: TaskStatusEnum
    download_url: Optional[str] = None
