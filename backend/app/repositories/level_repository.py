from sqlalchemy.orm import Session

from app.models.level import Level


class LevelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, level: Level) -> Level:
        self.db.add(level)
        self.db.commit()
        self.db.refresh(level)
        return level

    def list_all(self) -> list[Level]:
        return (
            self.db.query(Level)
            .order_by(Level.level_number.asc())
            .all()
        )

    def list_by_game(self, game_id: int) -> list[Level]:
        return (
            self.db.query(Level)
            .filter(Level.game_id == game_id)
            .order_by(Level.level_number.asc())
            .all()
        )

    def list_active_by_game(self, game_id: int) -> list[Level]:
        return (
            self.db.query(Level)
            .filter(
                Level.game_id == game_id,
                Level.is_active.is_(True),
            )
            .order_by(Level.level_number.asc())
            .all()
        )

    def get_by_id(self, level_id: int) -> Level | None:
        return (
            self.db.query(Level)
            .filter(Level.id == level_id)
            .first()
        )

    def get_by_game_and_number(
        self,
        game_id: int,
        level_number: int,
    ) -> Level | None:
        return (
            self.db.query(Level)
            .filter(
                Level.game_id == game_id,
                Level.level_number == level_number,
            )
            .first()
        )

    def get_next_level(
        self,
        game_id: int,
        current_level_number: int,
    ) -> Level | None:
        return (
            self.db.query(Level)
            .filter(
                Level.game_id == game_id,
                Level.level_number == current_level_number + 1,
                Level.is_active.is_(True),
            )
            .first()
        )

    def save(self, level: Level) -> Level:
        self.db.commit()
        self.db.refresh(level)
        return level

    def delete(self, level: Level) -> None:
        self.db.delete(level)
        self.db.commit()
