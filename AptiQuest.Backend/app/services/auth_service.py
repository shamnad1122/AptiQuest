from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginRequest, LoginResponse


class AuthService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def login(self, login_data: LoginRequest) -> LoginResponse:

        user = self.repository.get_by_email(
            login_data.email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        password_valid = verify_password(
            login_data.password,
            user.password_hash
        )

        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            user_id=user.user_id,
            username=user.username
        )

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.jwt_access_token_expire_minutes * 60
        )