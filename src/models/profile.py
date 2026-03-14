from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .user import User


class Profile(Base):
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    photo: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )
    user: Mapped["User"] = relationship(
        back_populates="profile",
        foreign_keys=[user_id],
    )
