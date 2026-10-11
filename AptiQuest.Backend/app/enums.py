from enum import StrEnum


class DifficultyLevel(StrEnum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class QuestionType(StrEnum):
    MCQ = "MCQ"
    MULTIPLE_SELECT = "MultipleSelect"
    TRUE_FALSE = "TrueFalse"
    FILL_IN_THE_BLANK = "FillInTheBlank"


class UserRole(StrEnum):
    USER = "User"
    ADMIN = "Admin"
