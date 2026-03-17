from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .profile import Profile


class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    reset_password: Mapped[str] = mapped_column(nullable=True)  # нужное поле?
    confirm_code: Mapped[str] = mapped_column(nullable=True)  # нужное поле?
    is_superuser: Mapped[bool] = mapped_column(default=False)

    profile: Mapped["Profile"] = relationship(back_populates="user")
