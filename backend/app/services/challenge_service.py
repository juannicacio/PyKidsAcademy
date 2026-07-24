from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.challenge import Challenge
from app.repositories.challenge_repository import ChallengeRepository
from app.repositories.level_repository import LevelRepository
from app.schemas.challenge import ChallengeCreate, ChallengeUpdate


class ChallengeService:
    def __init__(self, db: Session):
        self.challenge_repository = ChallengeRepository(db)
        self.level_repository = LevelRepository(db)

    def create_challenge(self, challenge_data: ChallengeCreate) -> Challenge:
        level = self.level_repository.get_by_id(challenge_data.level_id)

        if not level:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Level not found.",
            )

        existing = self.challenge_repository.get_by_level_and_order(
            challenge_data.level_id,
            challenge_data.challenge_order,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Challenge order already exists for this level.",
            )

        challenge = Challenge(**challenge_data.model_dump())

        return self.challenge_repository.create(challenge)

    def list_challenges(self):
        return self.challenge_repository.list_all()

    def list_by_level(self, level_id: int):
        return self.challenge_repository.list_by_level(level_id)

    def list_active_by_level(self, level_id: int):
        return self.challenge_repository.list_active_by_level(level_id)

    def get_challenge_or_404(self, challenge_id: int) -> Challenge:
        challenge = self.challenge_repository.get_by_id(challenge_id)

        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Challenge not found.",
            )

        return challenge

    def update_challenge(
        self,
        challenge_id: int,
        challenge_data: ChallengeUpdate,
    ) -> Challenge:
        challenge = self.get_challenge_or_404(challenge_id)

        update_data = challenge_data.model_dump(exclude_unset=True)

        if "challenge_order" in update_data:
            existing = self.challenge_repository.get_by_level_and_order(
                challenge.level_id,
                update_data["challenge_order"],
            )

            if existing and existing.id != challenge.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Challenge order already exists for this level.",
                )

        for field, value in update_data.items():
            setattr(challenge, field, value)

        return self.challenge_repository.save(challenge)

    def delete_challenge(self, challenge_id: int) -> None:
        challenge = self.get_challenge_or_404(challenge_id)

        self.challenge_repository.delete(challenge)
