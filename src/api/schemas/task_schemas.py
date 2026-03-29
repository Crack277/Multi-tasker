from datetime import datetime

from pydantic import BaseModel


class TaskCreate(BaseModel):
    assignee_id: int
    project_id: int
    category_id: int

    title: str
    description: str
    priority: str  # type?
    status: str  # type?
    deadline: datetime
    created_at: datetime = datetime.now()
    updated_at: datetime


class BaseTask(TaskCreate):
    author_id: int
