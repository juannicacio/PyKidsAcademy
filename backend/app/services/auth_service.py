from sqlalchemy.orm import Session

from app.auth.hashing import verify_password
from app.auth.jwt import create_access_token
from app.exceptions import InvalidCredentials
from app.repositories.user_repository import UserRepository


def login_user(
    db: Session,
    email: str,
    password: str,
):
    user = UserRepository.get_by_email(
        db,
        email,
    )

    if user is None:
        raise InvalidCredentials()

    if not verify_password(
        password,
        user.password_hash,
    ):
        raise InvalidCredentials()

    token = create_access_token(
        {
            "sub": user.email,
            "role": user.role,
            "user_id": user.id,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
