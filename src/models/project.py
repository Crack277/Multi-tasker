from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .task import Task
    from .user import User


class Project(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    icon: Mapped[str | None] = mapped_column(String(100), nullable=True)

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )

    owner: Mapped["User"] = relationship(
        back_populates="project",
        foreign_keys=[owner_id],
    )

    task: Mapped[List["Task"]] = relationship(back_populates="project")
