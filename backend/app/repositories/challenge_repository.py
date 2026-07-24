from sqlalchemy.orm import Session

from app.models.challenge import Challenge


class ChallengeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, challenge: Challenge) -> Challenge:
        self.db.add(challenge)
        self.db.commit()
        self.db.refresh(challenge)
        return challenge

    def list_all(self) -> list[Challenge]:
        return (
            self.db.query(Challenge)
            .order_by(
                Challenge.level_id,
                Challenge.challenge_order,
            )
            .all()
        )

    def list_by_level(self, level_id: int) -> list[Challenge]:
        return (
            self.db.query(Challenge)
            .filter(Challenge.level_id == level_id)
            .order_by(Challenge.challenge_order)
            .all()
        )

    def list_active_by_level(self, level_id: int) -> list[Challenge]:
        return (
            self.db.query(Challenge)
            .filter(
                Challenge.level_id == level_id,
                Challenge.is_active.is_(True),
            )
            .order_by(Challenge.challenge_order)
            .all()
        )

    def get_by_id(self, challenge_id: int) -> Challenge | None:
        return (
            self.db.query(Challenge)
            .filter(Challenge.id == challenge_id)
            .first()
        )

    def get_by_level_and_order(
        self,
        level_id: int,
        challenge_order: int,
    ) -> Challenge | None:
        return (
            self.db.query(Challenge)
            .filter(
                Challenge.level_id == level_id,
                Challenge.challenge_order == challenge_order,
            )
            .first()
        )

    def save(self, challenge: Challenge) -> Challenge:
        self.db.commit()
        self.db.refresh(challenge)
        return challenge

    def delete(self, challenge: Challenge) -> None:
        self.db.delete(challenge)
        self.db.commit()
