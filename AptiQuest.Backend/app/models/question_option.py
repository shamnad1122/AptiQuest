from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class QuestionOption(Base):
    __tablename__ = "QuestionOptions"

    option_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey("Questions.question_id"),
        nullable=False,
        index=True
    )

    option_text: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    option_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    question = relationship(
        "Question",
        back_populates="options"
    )