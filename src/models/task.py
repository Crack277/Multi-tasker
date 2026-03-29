from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .category import Category
    from .project import Project
    from .user import User


class Task(Base):
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    priority: Mapped[str] = mapped_column(String(100), nullable=False)  # Mapped[type?]
    status: Mapped[str] = mapped_column(String(100), nullable=False)  # Mapped[type?]

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
