import math

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.user import User
from app.repositories.question_repository import QuestionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.question_schema import (
    QuestionCreate,
    QuestionListResponse,
    QuestionListItem,
    QuestionResponse,
    QuestionUpdate,
    QuestionOptionResponse,
    PracticeQuestionListResponse,
    PracticeQuestionResponse,
    AnswerFeedback,
)


class QuestionService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = QuestionRepository(db)
        self.user_repository = UserRepository(db)

    def list_practice_questions(self, page=1, page_size=20, subtopic_id=None,
                                topic_id=None, difficulty=None, offset=None):
        if subtopic_id is not None:
            from app.models.subtopic import SubTopic
            subtopic = self.db.get(SubTopic, subtopic_id)
            if subtopic is None or not subtopic.is_active:
                raise HTTPException(status_code=404, detail="Subtopic not found")
            if topic_id is not None and topic_id != subtopic.topic_id:
                raise HTTPException(status_code=400, detail="subtopic_id does not belong to topic_id")
        if topic_id is not None:
            topic = self.repository.get_topic(topic_id)
            if topic is None or not topic.is_active:
                raise HTTPException(status_code=404, detail="Topic not found")
        total = self.repository.count_practice_questions(subtopic_id, topic_id, difficulty)
        items = self.repository.get_practice_questions(page, page_size, subtopic_id, topic_id, difficulty, offset)
        return PracticeQuestionListResponse(
            items=[PracticeQuestionResponse.model_validate(q) for q in items], limit=page_size,
            offset=offset if offset is not None else (page - 1) * page_size,
            total=total, total_pages=max(1, math.ceil(total / page_size)))

    def count_practice_questions(self, subtopic_id=None, topic_id=None, difficulty=None):
        if subtopic_id is not None:
            from app.models.subtopic import SubTopic
            subtopic = self.db.get(SubTopic, subtopic_id)
            if subtopic is None or not subtopic.is_active:
                raise HTTPException(status_code=404, detail="Subtopic not found")
            if topic_id is not None and topic_id != subtopic.topic_id:
                raise HTTPException(status_code=400, detail="subtopic_id does not belong to topic_id")
        if topic_id is not None:
            topic = self.repository.get_topic(topic_id)
            if topic is None or not topic.is_active:
                raise HTTPException(status_code=404, detail="Topic not found")
        return self.repository.count_practice_questions(subtopic_id, topic_id, difficulty)

    def submit_answer(self, question_id: int, option_id: int):
        question = self.repository.get_by_id_active(question_id)
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        selected = self.repository.get_option(question_id, option_id)
        if selected is None:
            raise HTTPException(status_code=404, detail="Option not found for this question")
        correct = self.repository.get_correct_option(question_id)
        if correct is None:
            raise HTTPException(status_code=500, detail="Question has no valid answer")
        return AnswerFeedback(question_id=question_id, selected_option_id=option_id,
            selected_answer=selected.option_text, is_correct=(selected.option_id == correct.option_id),
            correct_option_id=correct.option_id, correct_answer=correct.option_text,
            explanation=question.explanation)

    def list_topics(self):
        return self.repository.get_topics()

    def list_subtopics(self, topic_id: int):
        topic = self.repository.get_topic(topic_id)
        if topic is None:
            raise HTTPException(status_code=404, detail="Topic not found")
        if not topic.is_active:
            return []
        return self.repository.get_subtopics(topic_id)

    def create_question(
        self,
        data: QuestionCreate,
        current_user: User
    ) -> Question:

        self._validate_subtopic_exists(data.subtopic_id)

        question = Question(
            subtopic_id=data.subtopic_id,
            question_text=data.question_text,
            question_type=data.question_type,
            explanation=data.explanation,
            hint=data.hint,
            difficulty=data.difficulty,
            expected_time_seconds=data.expected_time_seconds,
            created_by=current_user.user_id,
            is_active=True
        )

        self.repository.create(question)

        options = [
            QuestionOption(
                question_id=question.question_id,
                option_text=opt.option_text,
                option_order=opt.option_order,
                is_correct=opt.is_correct
            )
            for opt in data.options
        ]

        self.repository.create_options(options)

        self.db.commit()
        self.db.refresh(question)

        return question

    def get_question(self, question_id: int) -> Question:

        question = self.repository.get_by_id_active(question_id)

        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )

        return question

    def get_question_for_update(self, question_id: int) -> Question:

        question = self.repository.get_by_id(question_id)

        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )

        return question

    def list_questions(
        self,
        page: int = 1,
        page_size: int = 20,
        subtopic_id: int | None = None,
        topic_id: int | None = None,
        difficulty: str | None = None,
        question_type: str | None = None,
        is_active: bool | None = None,
        search: str | None = None
    ) -> QuestionListResponse:

        total = self.repository.count_filtered(
            subtopic_id=subtopic_id,
            topic_id=topic_id,
            difficulty=difficulty,
            question_type=question_type,
            is_active=is_active,
            search=search
        )

        total_pages = math.ceil(total / page_size) if total > 0 else 1

        items = self.repository.get_filtered(
            page=page,
            page_size=page_size,
            subtopic_id=subtopic_id,
            topic_id=topic_id,
            difficulty=difficulty,
            question_type=question_type,
            is_active=is_active,
            search=search
        )

        return QuestionListResponse(
            items=[
                QuestionListItem.model_validate(item)
                for item in items
            ],
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages
        )

    def update_question(
        self,
        question_id: int,
        data: QuestionUpdate,
        current_user: User
    ) -> Question:

        question = self.get_question_for_update(question_id)

        self._check_permission(question, current_user)
        self._validate_subtopic_exists(data.subtopic_id)

        question.subtopic_id = data.subtopic_id
        question.question_text = data.question_text
        question.question_type = data.question_type
        question.explanation = data.explanation
        question.hint = data.hint
        question.difficulty = data.difficulty
        question.expected_time_seconds = data.expected_time_seconds

        self.repository.delete_options_by_question(question_id)

        new_options = [
            QuestionOption(
                question_id=question_id,
                option_text=opt.option_text,
                option_order=opt.option_order,
                is_correct=opt.is_correct
            )
            for opt in data.options
        ]

        self.repository.create_options(new_options)

        self.db.commit()
        self.db.refresh(question)

        return question

    def delete_question(
        self,
        question_id: int,
        current_user: User
    ) -> None:

        question = self.get_question_for_update(question_id)
        self._check_permission(question, current_user)

        self.repository.soft_delete(question)
        self.db.commit()

    def _validate_subtopic_exists(self, subtopic_id: int) -> None:

        from app.models.subtopic import SubTopic
        from sqlalchemy import select

        statement = select(SubTopic).where(
            SubTopic.subtopic_id == subtopic_id
        )
        subtopic = self.db.scalar(statement)

        if subtopic is None or not subtopic.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subtopic does not exist or is inactive"
            )
        if not subtopic.topic.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subtopic belongs to an inactive topic"
            )

    def _check_permission(
        self,
        question: Question,
        current_user: User
    ) -> None:

        is_admin = current_user.role == "Admin"
        is_creator = (
            question.created_by is not None
            and question.created_by == current_user.user_id
        )

        if not is_admin and not is_creator:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to modify this question"
            )
