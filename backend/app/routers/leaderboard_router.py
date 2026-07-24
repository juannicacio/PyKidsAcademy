from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.leaderboard import LeaderboardEntry
from app.services.leaderboard_service import LeaderboardService

router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboard"],
)


@router.get(
    "/xp",
    response_model=list[LeaderboardEntry],
)
def leaderboard_by_xp(
    db: Session = Depends(get_db),
):
    return LeaderboardService(db).by_xp()


@router.get(
    "/coins",
    response_model=list[LeaderboardEntry],
)
def leaderboard_by_coins(
    db: Session = Depends(get_db),
):
    return LeaderboardService(db).by_coins()


@router.get(
    "/level",
    response_model=list[LeaderboardEntry],
)
def leaderboard_by_level(
    db: Session = Depends(get_db),
):
    return LeaderboardService(db).by_level()
