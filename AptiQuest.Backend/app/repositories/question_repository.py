import math

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.subtopic import SubTopic
from app.models.topic import Topic


class QuestionRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, question_id: int) -> Question | None:
        statement = (
            select(Question)
            .options(selectinload(Question.options))
            .where(Question.question_id == question_id)
        )

        return self.db.scalar(statement)

    def get_by_id_active(self, question_id: int) -> Question | None:
        statement = (
            select(Question)
            .options(selectinload(Question.options))
            .where(
                Question.question_id == question_id,
                Question.is_active == True
            )
        )

        return self.db.scalar(statement)

    def create(self, question: Question) -> Question:
        self.db.add(question)
        self.db.flush()

        return question

    def create_options(
        self, options: list[QuestionOption]
    ) -> list[QuestionOption]:
        self.db.add_all(options)
        self.db.flush()

        return options

    def update(self, question: Question) -> Question:
        self.db.flush()

        return question

    def delete_options_by_question(self, question_id: int) -> None:
        statement = select(QuestionOption).where(
            QuestionOption.question_id == question_id
        )
        options = self.db.scalars(statement).all()

        for option in options:
            self.db.delete(option)

        self.db.flush()

    def count_filtered(
        self,
        subtopic_id: int | None = None,
        topic_id: int | None = None,
        difficulty: str | None = None,
        question_type: str | None = None,
        is_active: bool | None = None,
        search: str | None = None
    ) -> int:
        statement = select(func.count(Question.question_id))
        statement = self._apply_filters(
            statement, subtopic_id, topic_id, difficulty,
            question_type, is_active, search
        )

        return self.db.scalar(statement)

    def get_filtered(
        self,
        page: int = 1,
        page_size: int = 20,
        subtopic_id: int | None = None,
        topic_id: int | None = None,
        difficulty: str | None = None,
        question_type: str | None = None,
        is_active: bool | None = None,
        search: str | None = None
    ) -> list[Question]:
        statement = select(Question)
        statement = self._apply_filters(
            statement, subtopic_id, topic_id, difficulty,
            question_type, is_active, search
        )

        statement = statement.order_by(Question.question_id.desc())

        offset = (page - 1) * page_size
        statement = statement.offset(offset).limit(page_size)

        return list(self.db.scalars(statement).all())

    def soft_delete(self, question: Question) -> None:
        question.is_active = False
        self.db.flush()

    def _apply_filters(
        self,
        statement,
        subtopic_id: int | None = None,
        topic_id: int | None = None,
        difficulty: str | None = None,
        question_type: str | None = None,
        is_active: bool | None = None,
        search: str | None = None
    ):
        if subtopic_id is not None:
            statement = statement.where(
                Question.subtopic_id == subtopic_id
            )

        if topic_id is not None:
            statement = (
                statement.join(SubTopic)
                .join(Topic)
                .where(Topic.topic_id == topic_id)
            )

        if difficulty is not None:
            statement = statement.where(
                Question.difficulty == difficulty
            )

        if question_type is not None:
            statement = statement.where(
                Question.question_type == question_type
            )

        if is_active is not None:
            statement = statement.where(
                Question.is_active == is_active
            )

        if search is not None:
            search_pattern = f"%{search}%"
            statement = statement.where(
                Question.question_text.ilike(search_pattern)
            )

        return statement
