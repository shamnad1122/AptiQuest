from pydantic import BaseModel, ConfigDict, Field, model_validator


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
    subtopic_id: int
    question_text: str = Field(
        min_length=1
    )
    question_type: str = Field(
        default="MCQ",
        pattern=r"^MCQ$"
    )
    explanation: str | None = None
    hint: str | None = None
    difficulty: str = Field(
        default="Easy",
        pattern=r"^(Easy|Medium|Hard)$"
    )
    expected_time_seconds: int | None = Field(
        default=None,
        gt=0
    )
    options: list[QuestionOptionCreate] = Field(
        min_length=4,
        max_length=4
    )

    @model_validator(mode="after")
    def validate_mcq_options(self):
        if self.question_type == "MCQ":
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


class QuestionUpdate(BaseModel):
    subtopic_id: int
    question_text: str = Field(
        min_length=1
    )
    question_type: str = Field(
        default="MCQ",
        pattern=r"^MCQ$"
    )
    explanation: str | None = None
    hint: str | None = None
    difficulty: str = Field(
        default="Easy",
        pattern=r"^(Easy|Medium|Hard)$"
    )
    expected_time_seconds: int | None = Field(
        default=None,
        gt=0
    )
    options: list[QuestionOptionUpdate] = Field(
        min_length=4,
        max_length=4
    )

    @model_validator(mode="after")
    def validate_mcq_options(self):
        if self.question_type == "MCQ":
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
