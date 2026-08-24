from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.question_schema import (
    QuestionAdminResponse,
    QuestionCreate,
    QuestionListResponse,
    QuestionResponse,
    QuestionUpdate,
)
from app.services.question_service import QuestionService


router = APIRouter(
    prefix="/api/questions",
    tags=["Questions"]
)


@router.post(
    "",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = QuestionService(db)
    question = service.create_question(question_data, current_user)
    return QuestionResponse.model_validate(question)


@router.get(
    "",
    response_model=QuestionListResponse
)
def list_questions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    topic_id: int | None = Query(default=None),
    subtopic_id: int | None = Query(default=None),
    difficulty: str | None = Query(default=None),
    question_type: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = QuestionService(db)
    return service.list_questions(
        page=page,
        page_size=page_size,
        topic_id=topic_id,
        subtopic_id=subtopic_id,
        difficulty=difficulty,
        question_type=question_type,
        is_active=is_active,
        search=search
    )


@router.get(
    "/{question_id}",
    response_model=QuestionResponse
)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = QuestionService(db)
    question = service.get_question(question_id)
    return QuestionResponse.model_validate(question)


@router.put(
    "/{question_id}",
    response_model=QuestionResponse
)
def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = QuestionService(db)
    question = service.update_question(
        question_id, question_data, current_user
    )
    return QuestionResponse.model_validate(question)


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = QuestionService(db)
    service.delete_question(question_id, current_user)
