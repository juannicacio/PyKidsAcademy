from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.auth.jwt import decode_access_token
from app.core.database import get_db
from app.exceptions import InvalidToken
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")

        if email is None:
            raise InvalidToken()

    except JWTError:
        raise InvalidToken()

    user = UserRepository.get_by_email(
        db,
        email,
    )

    if user is None:
        raise InvalidToken()

    return user
