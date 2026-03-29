from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .task import Task
    from .user import User


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    marker: Mapped[str] = mapped_column(String(7), nullable=False)  # HEX цвет (#cac4b0)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="category",
        foreign_keys=[user_id],
    )

    task: Mapped[List["Task"]] = relationship(back_populates="category")
