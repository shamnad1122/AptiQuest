import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace

from pydantic import ValidationError

from app.enums import DifficultyLevel, QuestionType, UserRole
from app.core.security import get_current_user
from app.schemas.auth_schema import LoginRequest
from app.schemas.question_schema import QuestionCreate
from app.schemas.user_schema import UserCreate
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from fastapi.security import HTTPAuthorizationCredentials


class QuestionEnumSchemaTests(unittest.TestCase):
    def valid_question(self, **overrides):
        payload = {
            "subtopic_id": 1,
            "question_text": "Choose the correct answer",
            "options": [
                {"option_text": "First", "option_order": 1, "is_correct": True},
                {"option_text": "Second", "option_order": 2, "is_correct": False},
                {"option_text": "Third", "option_order": 3, "is_correct": False},
                {"option_text": "Fourth", "option_order": 4, "is_correct": False},
            ],
        }
        payload.update(overrides)
        return payload

    def test_accepts_centralized_supported_values(self):
        question = QuestionCreate.model_validate(self.valid_question(
            difficulty=DifficultyLevel.HARD,
            question_type=QuestionType.MCQ,
        ))
        self.assertEqual(question.difficulty, DifficultyLevel.HARD)
        self.assertEqual(question.question_type, QuestionType.MCQ)
        self.assertEqual(UserRole.USER.value, "User")

    def test_rejects_unknown_difficulty(self):
        with self.assertRaises(ValidationError):
            QuestionCreate.model_validate(self.valid_question(difficulty="Extreme"))

    def test_rejects_declared_but_unsupported_question_types(self):
        for question_type in (
            QuestionType.MULTIPLE_SELECT,
            QuestionType.TRUE_FALSE,
            QuestionType.FILL_IN_THE_BLANK,
        ):
            with self.subTest(question_type=question_type):
                with self.assertRaises(ValidationError):
                    QuestionCreate.model_validate(self.valid_question(question_type=question_type))

    def test_registration_assigns_the_existing_user_role(self):
        service = UserService(db=None)
        repository = Mock()
        repository.get_by_email.return_value = None
        repository.get_by_username.return_value = None
        repository.create.side_effect = lambda user: user
        service.repository = repository
        user_data = UserCreate(
            first_name="Apti",
            username="aptitest",
            email="apti@example.com",
            password="secure-password",
        )

        with patch("app.services.user_service.hash_password", return_value="hashed"):
            user = service.create_user(user_data)

        self.assertEqual(user.role, UserRole.USER.value)

    def test_login_token_is_accepted_by_existing_jwt_dependency(self):
        user = SimpleNamespace(
            user_id=42,
            username="aptitest",
            email="apti@example.com",
            password_hash="hashed",
            is_active=True,
        )
        service = AuthService(db=None)
        service.repository = Mock()
        service.repository.get_by_email.return_value = user

        with patch("app.services.auth_service.verify_password", return_value=True):
            login_response = service.login(LoginRequest(
                email="apti@example.com", password="secure-password"
            ))

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials=login_response.access_token
        )
        with patch("app.repositories.user_repository.UserRepository") as repository:
            repository.return_value.get_by_id.return_value = user
            authenticated_user = get_current_user(credentials, db=None)

        self.assertIs(authenticated_user, user)


if __name__ == "__main__":
    unittest.main()
