from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.level import (
    LevelCreate,
    LevelResponse,
    LevelUpdate,
)
from app.services.level_service import LevelService

router = APIRouter(
    prefix="/levels",
    tags=["Levels"],
)


@router.post(
    "",
    response_model=LevelResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_level(
    data: LevelCreate,
    db: Session = Depends(get_db),
):
    service = LevelService(db)
    return service.create_level(data)


@router.get(
    "",
    response_model=list[LevelResponse],
)
def list_levels(
    db: Session = Depends(get_db),
):
    service = LevelService(db)
    return service.list_levels()


@router.get(
    "/game/{game_id}",
    response_model=list[LevelResponse],
)
def list_levels_by_game(
    game_id: int,
    db: Session = Depends(get_db),
):
    service = LevelService(db)
    return service.list_levels_by_game(game_id)


@router.get(
    "/game/{game_id}/active",
    response_model=list[LevelResponse],
)
def list_active_levels_by_game(
    game_id: int,
    db: Session = Depends(get_db),
):
    service = LevelService(db)
    return service.list_active_levels_by_game(game_id)


@router.get(
    "/{level_id}",
    response_model=LevelResponse,
)
def get_level(
    level_id: int,
    db: Session = Depends(get_db),
):
    service = LevelService(db)
    return service.get_level_or_404(level_id)


@router.put(
    "/{level_id}",
    response_model=LevelResponse,
)
def update_level(
    level_id: int,
    data: LevelUpdate,
    db: Session = Depends(get_db),
):
    service = LevelService(db)
    return service.update_level(level_id, data)


@router.delete(
    "/{level_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_level(
    level_id: int,
    db: Session = Depends(get_db),
):
    service = LevelService(db)
    service.delete_level(level_id)
