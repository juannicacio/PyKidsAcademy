from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.achievement import (
    AchievementCreate,
    AchievementResponse,
    AchievementUpdate,
)
from app.services.achievement_service import AchievementService

router = APIRouter(
    prefix="/achievements",
    tags=["Achievements"],
)


@router.post(
    "",
    response_model=AchievementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_achievement(
    achievement: AchievementCreate,
    db: Session = Depends(get_db),
):
    service = AchievementService(db)

    try:
        return service.create(achievement)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[AchievementResponse],
)
def list_achievements(
    db: Session = Depends(get_db),
):
    return AchievementService(db).list_all()


@router.get(
    "/active",
    response_model=list[AchievementResponse],
)
def list_active_achievements(
    db: Session = Depends(get_db),
):
    return AchievementService(db).list_active()


@router.get(
    "/{achievement_id}",
    response_model=AchievementResponse,
)
def get_achievement(
    achievement_id: int,
    db: Session = Depends(get_db),
):
    service = AchievementService(db)

    achievement = service.get_by_id(achievement_id)

    if achievement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found.",
        )

    return achievement


@router.put(
    "/{achievement_id}",
    response_model=AchievementResponse,
)
def update_achievement(
    achievement_id: int,
    data: AchievementUpdate,
    db: Session = Depends(get_db),
):
    service = AchievementService(db)

    achievement = service.get_by_id(achievement_id)

    if achievement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found.",
        )

    try:
        return service.update(
            achievement,
            data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


@router.delete(
    "/{achievement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_achievement(
    achievement_id: int,
    db: Session = Depends(get_db),
):
    service = AchievementService(db)

    achievement = service.get_by_id(achievement_id)

    if achievement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found.",
        )

    service.delete(achievement)
