from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.question_schema import (
    AnswerFeedback,
    AnswerSubmission,
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
    PracticeQuestionListResponse,
    PracticeQuestionResponse,
    TopicResponse,
    SubTopicResponse,
)
from app.services.question_service import QuestionService


router = APIRouter(
    prefix="/api/questions",
    tags=["Questions"]
)


@router.post(
    "",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a multiple-choice question",
    description="Creates an MCQ under an active subtopic. Requires authentication. Supply exactly four unique options with orders 1–4 and exactly one correct option."
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
    response_model=PracticeQuestionListResponse,
    summary="Browse practice questions",
    description="Lists active questions and options without exposing correctness or explanations."
)
def list_questions(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    topic_id: int | None = Query(default=None),
    subtopic_id: int | None = Query(default=None),
    difficulty: str | None = Query(default=None, pattern=r"^(Easy|Medium|Hard)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = QuestionService(db)
    return service.list_practice_questions(
        page=1,
        page_size=limit,
        topic_id=topic_id,
        subtopic_id=subtopic_id,
        difficulty=difficulty,
        offset=offset,
    )


@router.get("/count", response_model=int, summary="Count available practice questions")
def count_questions(topic_id: int | None = Query(default=None),
                    subtopic_id: int | None = Query(default=None),
                    difficulty: str | None = Query(default=None, pattern=r"^(Easy|Medium|Hard)$"),
                    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return QuestionService(db).count_practice_questions(subtopic_id, topic_id, difficulty)


@router.get(
    "/{question_id}",
    response_model=PracticeQuestionResponse
)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = QuestionService(db)
    question = service.get_question(question_id)
    return PracticeQuestionResponse.model_validate(question)


@router.post("/{question_id}/submit", response_model=AnswerFeedback, summary="Submit a practice answer",
             description="Checks the selected option on the server and returns immediate feedback. Requires authentication.")
def submit_answer(question_id: int, body: AnswerSubmission,
                  db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return QuestionService(db).submit_answer(question_id, body.selected_option_id)


topics_router = APIRouter(prefix="/api/topics", tags=["Topics"])


@topics_router.get("", response_model=list[TopicResponse], summary="List active topics")
def list_topics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return [TopicResponse.model_validate(t) for t in QuestionService(db).list_topics()]


@topics_router.get("/{topic_id}/subtopics", response_model=list[SubTopicResponse], summary="List active subtopics")
def list_subtopics(topic_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return [SubTopicResponse.model_validate(t) for t in QuestionService(db).list_subtopics(topic_id)]


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
