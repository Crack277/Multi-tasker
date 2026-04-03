from datetime import datetime, timezone

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator

from src.models.task import TaskPriority, TaskStatus


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

