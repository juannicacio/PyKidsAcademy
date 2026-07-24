from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.challenge import (
    ChallengeCreate,
    ChallengeResponse,
    ChallengeUpdate,
)
from app.services.challenge_service import ChallengeService

router = APIRouter(
    prefix="/challenges",
    tags=["Challenges"],
)


@router.post(
    "",
    response_model=ChallengeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_challenge(
    challenge: ChallengeCreate,
    db: Session = Depends(get_db),
):
    service = ChallengeService(db)
    return service.create_challenge(challenge)


@router.get(
    "",
    response_model=List[ChallengeResponse],
)
def list_challenges(
    db: Session = Depends(get_db),
):
    service = ChallengeService(db)
    return service.list_challenges()


@router.get(
    "/level/{level_id}",
    response_model=List[ChallengeResponse],
)
def list_challenges_by_level(
    level_id: int,
    db: Session = Depends(get_db),
):
    service = ChallengeService(db)
    return service.list_by_level(level_id)


@router.get(
    "/level/{level_id}/active",
    response_model=List[ChallengeResponse],
)
def list_active_challenges(
    level_id: int,
    db: Session = Depends(get_db),
):
    service = ChallengeService(db)
    return service.list_active_by_level(level_id)


@router.get(
    "/{challenge_id}",
    response_model=ChallengeResponse,
)
def get_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
):
    service = ChallengeService(db)
    return service.get_challenge_or_404(challenge_id)


@router.put(
    "/{challenge_id}",
    response_model=ChallengeResponse,
)
def update_challenge(
    challenge_id: int,
    challenge: ChallengeUpdate,
    db: Session = Depends(get_db),
):
    service = ChallengeService(db)
    return service.update_challenge(
        challenge_id,
        challenge,
    )


@router.delete(
    "/{challenge_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
):
    service = ChallengeService(db)
    service.delete_challenge(challenge_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
