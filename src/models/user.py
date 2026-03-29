from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .category import Category
    from .profile import Profile
    from .project import Project
    from .task import Task


class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    confirm_code: Mapped[str] = mapped_column(nullable=True)  # нужное поле?
    is_superuser: Mapped[bool] = mapped_column(default=False)

    profile: Mapped["Profile"] = relationship(back_populates="user")
    project: Mapped[List["Project"]] = relationship(back_populates="owner")
    category: Mapped[List["Category"]] = relationship(back_populates="user")
    task_created: Mapped[List["Task"]] = relationship(
        back_populates="author",
        foreign_keys="Task.author_id",
    )
    task_assigned: Mapped[List["Task"]] = relationship(
        back_populates="assignee",
        foreign_keys="Task.assignee_id",
    )
