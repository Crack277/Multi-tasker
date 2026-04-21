from datetime import datetime, timezone

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator

from enum import StrEnum, Enum


class TaskTypes(StrEnum):
    VERY_URGENT = "very_urgent"  # очень срочно (красный)
    URGENT = "urgent"  # срочно (оранжевый)
    CAN_WAIT = "can_wait"  # может подождать (желтый)
    NOT_URGENT = "not_urgent"  # не срочно (зеленый)


class TaskPriority(str, Enum):
    VERY_URGENT = "very_urgent"
    URGENT = "urgent"
    CAN_WAIT = "can_wait"
    NOT_URGENT = "not_urgent"


class TaskStatus(str, Enum):
    IN_PROGRESS = "in_progress"  # в работе
    COMPLETED = "completed"  # выполнена

class TaskCreate(BaseModel):
    assignee_id: int
    project_id: int
    category_id: int

    title: str
    description: str
    priority: TaskPriority = Field(default=TaskPriority.NOT_URGENT)
    status: TaskStatus = Field(default=TaskStatus.IN_PROGRESS)
    deadline: datetime = (
        datetime.now(timezone.utc).replace(tzinfo=None).replace(microsecond=0)
    )

    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, v: datetime) -> datetime:
        if v < datetime.now(timezone.utc).replace(tzinfo=None).replace(microsecond=0):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Deadline should not be in the past!",
            )
        return v


class UserTasksInfo(BaseModel):
    all_tasks: int
    completed_tasks: int

