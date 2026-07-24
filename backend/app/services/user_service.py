from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.exceptions import EmailAlreadyExists
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest


def create_user(
    db: Session,
    user: RegisterRequest,
) -> User:

    email = user.email.lower().strip()

    existing = UserRepository.get_by_email(
        db,
        email,
    )

    if existing:
        raise EmailAlreadyExists()

    db_user = User(
        email=email,
        password_hash=hash_password(user.password),
        role="parent",
        country=user.country.upper(),
        language=user.language.value,
        max_students=2,
    )

    return UserRepository.create(
        db,
        db_user,
    )
