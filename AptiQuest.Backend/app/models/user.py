from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "Users"

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    profile_image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="User"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_questions = relationship(
        "Question",
        back_populates="created_by_user"
    )