from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .profile import Profile


class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]  # 8 - 16 символов ?
    reset_password: Mapped[str] = mapped_column(nullable=True)
    confirm_code: Mapped[str] = mapped_column(nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    profile: Mapped["Profile"] = relationship(back_populates="user")
