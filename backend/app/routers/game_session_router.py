from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.game_session import (
    GameSessionCreate,
    GameSessionResponse,
    GameSessionUpdate,
)
from app.services.game_session_service import GameSessionService

router = APIRouter(
    prefix="/game-sessions",
    tags=["Game Sessions"],
)


@router.post(
    "",
    response_model=GameSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_game_session(
    data: GameSessionCreate,
    db: Session = Depends(get_db),
):
    return GameSessionService(db).create(data)


@router.get(
    "",
    response_model=list[GameSessionResponse],
)
def list_game_sessions(
    db: Session = Depends(get_db),
):
    return GameSessionService(db).list_all()


@router.get(
    "/{session_id}",
    response_model=GameSessionResponse,
)
def get_game_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    return GameSessionService(db).get(session_id)


@router.get(
    "/student/{student_id}",
    response_model=list[GameSessionResponse],
)
def list_student_sessions(
    student_id: int,
    db: Session = Depends(get_db),
):
    return GameSessionService(db).list_by_student(student_id)


@router.put(
    "/{session_id}/finish",
    response_model=GameSessionResponse,
)
def finish_game_session(
    session_id: int,
    data: GameSessionUpdate,
    db: Session = Depends(get_db),
):
    return GameSessionService(db).finish(session_id, data)


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_game_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    GameSessionService(db).delete(session_id)
