from sqlalchemy.orm import Session

from app.repositories.leaderboard_repository import (
    LeaderboardRepository,
)
from app.schemas.leaderboard import LeaderboardEntry


class LeaderboardService:
    def __init__(self, db: Session):
        self.repository = LeaderboardRepository(db)

    def _serialize(self, students):
        return [
            LeaderboardEntry(
                student_id=s.id,
                first_name=s.first_name,
                avatar=s.avatar,
                learning_level=s.learning_level,
                xp=s.xp,
                coins=s.coins,
            )
            for s in students
        ]

    def by_xp(self):
        return self._serialize(
            self.repository.by_xp()
        )

    def by_coins(self):
        return self._serialize(
            self.repository.by_coins()
        )

    def by_level(self):
        return self._serialize(
            self.repository.by_level()
        )
