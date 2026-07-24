from sqlalchemy.orm import Session

from app.models.game import Game


class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, game: Game) -> Game:
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game

    def list_all(self) -> list[Game]:
        return (
            self.db.query(Game)
            .order_by(Game.title.asc())
            .all()
        )

    def list_active(self) -> list[Game]:
        return (
            self.db.query(Game)
            .filter(Game.is_active.is_(True))
            .order_by(Game.title.asc())
            .all()
        )

    def get_by_id(self, game_id: int) -> Game | None:
        return (
            self.db.query(Game)
            .filter(Game.id == game_id)
            .first()
        )

    def get_by_slug(self, slug: str) -> Game | None:
        return (
            self.db.query(Game)
            .filter(Game.slug == slug)
            .first()
        )

    def save(self, game: Game) -> Game:
        self.db.commit()
        self.db.refresh(game)
        return game

    def delete(self, game: Game) -> None:
        self.db.delete(game)
        self.db.commit()
