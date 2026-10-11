from pydantic import BaseModel, ConfigDict, Field, AliasChoices, field_validator, model_validator
from app.enums import DifficultyLevel, QuestionType


class QuestionOptionCreate(BaseModel):
    option_text: str = Field(
        min_length=1,
        max_length=500
    )
    option_order: int = Field(
        ge=1,
        le=4
    )
    is_correct: bool

    @field_validator("option_text", mode="before")
    @classmethod
    def normalize_option_text(cls, value):
        return value.strip() if isinstance(value, str) else value


class QuestionOptionUpdate(BaseModel):
    option_id: int | None = Field(
        default=None,
        description="Existing option ID to update. Omit to create a new option."
    )
    option_text: str = Field(
        min_length=1,
        max_length=500
    )
    option_order: int = Field(
        ge=1,
        le=4
    )
    is_correct: bool


class QuestionOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    option_id: int
    option_text: str
    option_order: int


class QuestionOptionAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    option_id: int
    option_text: str
    option_order: int
    is_correct: bool


class QuestionCreate(BaseModel):
    subtopic_id: int = Field(gt=0)
    question_text: str = Field(
        min_length=1,
        max_length=10000
    )
    question_type: QuestionType = QuestionType.MCQ
    explanation: str | None = None
    hint: str | None = None
    difficulty: DifficultyLevel = DifficultyLevel.EASY
    expected_time_seconds: int | None = Field(
        default=None,
        gt=0
    )
    options: list[QuestionOptionCreate] = Field(
        min_length=4,
        max_length=4
    )

    @field_validator("question_text", mode="before")
    @classmethod
    def normalize_question_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("explanation", "hint", mode="before")
    @classmethod
    def normalize_optional_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("question_type")
    @classmethod
    def require_supported_question_type(cls, value):
        if value != QuestionType.MCQ:
            raise ValueError("Only MCQ questions are currently supported")
        return value

    @model_validator(mode="after")
    def validate_mcq_options(self):
        if self.question_type == QuestionType.MCQ:
            orders = [opt.option_order for opt in self.options]
            if sorted(orders) != [1, 2, 3, 4]:
                raise ValueError(
                    "option_order must be 1, 2, 3, 4"
                )

            correct_count = sum(
                1 for opt in self.options if opt.is_correct
            )
            if correct_count != 1:
                raise ValueError(
                    "Exactly one option must have is_correct=true"
                )

            texts = [opt.option_text.strip() for opt in self.options]
            if any(t == "" for t in texts):
                raise ValueError(
                    "Option text cannot be empty"
                )

            normalized_texts = [text.casefold() for text in texts]
            if len(set(normalized_texts)) != 4:
                raise ValueError("Option texts must be unique")

        return self


class QuestionUpdate(BaseModel):
    subtopic_id: int
    question_text: str = Field(
        min_length=1
    )
    question_type: QuestionType = QuestionType.MCQ
    explanation: str | None = None
    hint: str | None = None
    difficulty: DifficultyLevel = DifficultyLevel.EASY
    expected_time_seconds: int | None = Field(
        default=None,
        gt=0
    )
    options: list[QuestionOptionUpdate] = Field(
        min_length=4,
        max_length=4
    )

    @field_validator("question_type")
    @classmethod
    def require_supported_question_type(cls, value):
        if value != QuestionType.MCQ:
            raise ValueError("Only MCQ questions are currently supported")
        return value

    @model_validator(mode="after")
    def validate_mcq_options(self):
        if self.question_type == QuestionType.MCQ:
            orders = [opt.option_order for opt in self.options]
            if sorted(orders) != [1, 2, 3, 4]:
                raise ValueError(
                    "option_order must be 1, 2, 3, 4"
                )

            correct_count = sum(
                1 for opt in self.options if opt.is_correct
            )
            if correct_count != 1:
                raise ValueError(
                    "Exactly one option must have is_correct=true"
                )

            texts = [opt.option_text.strip() for opt in self.options]
            if any(t == "" for t in texts):
                raise ValueError(
                    "Option text cannot be empty"
                )

        return self


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question_id: int
    subtopic_id: int
    question_text: str
    question_type: str
    explanation: str | None
    hint: str | None
    difficulty: str
    expected_time_seconds: int | None
    options: list[QuestionOptionResponse]


class QuestionListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question_id: int
    subtopic_id: int
    question_text: str
    question_type: str
    difficulty: str
    expected_time_seconds: int | None


class PracticeOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    option_id: int
    option_text: str
    option_order: int


class PracticeQuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    question_id: int
    subtopic_id: int
    question_text: str
    difficulty: str
    expected_time_seconds: int | None
    options: list[PracticeOptionResponse]


class PracticeQuestionListItem(PracticeQuestionResponse):
    pass


class PracticeQuestionListResponse(BaseModel):
    items: list[PracticeQuestionResponse]
    limit: int
    offset: int
    total: int
    total_pages: int


class AnswerSubmission(BaseModel):
    selected_option_id: int = Field(gt=0)


class AnswerFeedback(BaseModel):
    question_id: int
    selected_option_id: int
    selected_answer: str
    is_correct: bool
    correct_option_id: int
    correct_answer: str
    explanation: str | None


class TopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    topic_id: int
    topic_name: str = Field(validation_alias=AliasChoices("topic_name", "name"))
    description: str | None


class SubTopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    subtopic_id: int
    subtopic_name: str = Field(validation_alias=AliasChoices("subtopic_name", "name"))
    topic_id: int
    description: str | None


class QuestionAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question_id: int
    subtopic_id: int
    question_text: str
    question_type: str
    explanation: str | None
    hint: str | None
    difficulty: str
    expected_time_seconds: int | None
    created_by: int | None
    is_active: bool
    options: list[QuestionOptionAdminResponse]


class QuestionListResponse(BaseModel):
    items: list[QuestionListItem]
    page: int
    page_size: int
    total: int
    total_pages: int
