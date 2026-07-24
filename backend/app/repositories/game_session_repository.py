from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.game_session import GameSession
from app.schemas.game_session import (
    GameSessionCreate,
    GameSessionUpdate,
)


class GameSessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: GameSessionCreate) -> GameSession:
        session = GameSession(**data.model_dump())
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_by_id(self, session_id: int) -> GameSession | None:
        return (
            self.db.query(GameSession)
            .filter(GameSession.id == session_id)
            .first()
        )

    def list_all(self) -> list[GameSession]:
        return (
            self.db.query(GameSession)
            .order_by(GameSession.started_at.desc())
            .all()
        )

    def list_by_student(self, student_id: int) -> list[GameSession]:
        return (
            self.db.query(GameSession)
            .filter(GameSession.student_id == student_id)
            .order_by(GameSession.started_at.desc())
            .all()
        )

    def finish(
        self,
        session: GameSession,
        data: GameSessionUpdate,
    ) -> GameSession:
        values = data.model_dump()

        session.score = values["score"]
        session.correct_answers = values["correct_answers"]
        session.wrong_answers = values["wrong_answers"]
        session.xp_earned = values["xp_earned"]
        session.coins_earned = values["coins_earned"]
        session.completed = values["completed"]
        session.finished_at = datetime.now(UTC)

        self.db.commit()
        self.db.refresh(session)

        return session

    def delete(self, session: GameSession) -> None:
        self.db.delete(session)
        self.db.commit()
