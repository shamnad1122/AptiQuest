from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Question(Base):
    __tablename__ = "Questions"

    question_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    subtopic_id: Mapped[int] = mapped_column(
        ForeignKey("SubTopics.subtopic_id"),
        nullable=False,
        index=True
    )

    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    question_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="MCQ"
    )

    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    hint: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Easy"
    )

    expected_time_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("Users.user_id"),
        nullable=True,
        index=True
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

    subtopic = relationship(
        "SubTopic",
        back_populates="questions"
    )

    options = relationship(
        "QuestionOption",
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="QuestionOption.option_order"
    )

    created_by_user = relationship(
        "User",
        back_populates="created_questions"
    )