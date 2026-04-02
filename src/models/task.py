from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemy_Enum
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .category import Category
    from .project import Project
    from .user import User


class TaskPriority(str, Enum):
    VERY_URGENT = "very_urgent"  # очень срочно (красный)
    URGENT = "urgent"  # срочно (оранжевый)
    CAN_WAIT = "can_wait"  # может подождать (желтый)
    NOT_URGENT = "not_urgent"  # не срочно (зеленый)


class TaskStatus(str, Enum):
    IN_PROGRESS = "in_progress"  # в работе
    COMPLETED = "completed"  # выполнена


class Task(Base):
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    priority: Mapped[TaskPriority] = mapped_column(
        SQLAlchemy_Enum(TaskPriority),
        default=TaskPriority.NOT_URGENT,
        nullable=False,
    )
    status: Mapped[TaskStatus] = mapped_column(
        SQLAlchemy_Enum(TaskStatus),
        default=TaskStatus.IN_PROGRESS,
        nullable=False,
    )

    deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    assignee_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
    )

    author: Mapped["User"] = relationship(
        back_populates="task_created",
        foreign_keys=[author_id],
    )
    assignee: Mapped["User"] = relationship(
        back_populates="task_assigned",
        foreign_keys=[assignee_id],
    )
    project: Mapped["Project"] = relationship(
        back_populates="task",
        foreign_keys=[project_id],
    )
    category: Mapped["Category"] = relationship(
        back_populates="task",
        foreign_keys=[category_id],
    )
