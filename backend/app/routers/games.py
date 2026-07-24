from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.game import (
    GameCreate,
    GameResponse,
    GameUpdate,
)
from app.services.game_service import GameService

router = APIRouter(
    prefix="/games",
    tags=["Games"],
)


@router.post(
    "",
    response_model=GameResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_game(
    data: GameCreate,
    db: Session = Depends(get_db),
):
    service = GameService(db)
    return service.create_game(data)


@router.get(
    "",
    response_model=list[GameResponse],
)
def list_games(
    db: Session = Depends(get_db),
):
    service = GameService(db)
    return service.list_games()


@router.get(
    "/active",
    response_model=list[GameResponse],
)
def list_active_games(
    db: Session = Depends(get_db),
):
    service = GameService(db)
    return service.list_active_games()


@router.get(
    "/{game_id}",
    response_model=GameResponse,
)
def get_game(
    game_id: int,
    db: Session = Depends(get_db),
):
    service = GameService(db)
    return service.get_game_or_404(game_id)


@router.put(
    "/{game_id}",
    response_model=GameResponse,
)
def update_game(
    game_id: int,
    data: GameUpdate,
    db: Session = Depends(get_db),
):
    service = GameService(db)
    return service.update_game(game_id, data)


@router.delete(
    "/{game_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_game(
    game_id: int,
    db: Session = Depends(get_db),
):
    service = GameService(db)
    service.delete_game(game_id)
