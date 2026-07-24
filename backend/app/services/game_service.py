from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.game import Game
from app.repositories.game_repository import GameRepository
from app.schemas.game import GameCreate, GameUpdate


class GameService:
    def __init__(self, db: Session):
        self.repository = GameRepository(db)

    def create_game(self, data: GameCreate) -> Game:
        if self.repository.get_by_slug(data.slug):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Game slug already exists.",
            )

        if data.min_age > data.max_age:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum age cannot be greater than maximum age.",
            )

        game = Game(**data.model_dump())

        return self.repository.create(game)

    def list_games(self) -> list[Game]:
        return self.repository.list_all()

    def list_active_games(self) -> list[Game]:
        return self.repository.list_active()

    def get_game_or_404(self, game_id: int) -> Game:
        game = self.repository.get_by_id(game_id)

        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found.",
            )

        return game

    def update_game(
        self,
        game_id: int,
        data: GameUpdate,
    ) -> Game:
        game = self.get_game_or_404(game_id)

        values = data.model_dump(exclude_unset=True)

        if "slug" in values:
            existing = self.repository.get_by_slug(values["slug"])

            if existing and existing.id != game.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Game slug already exists.",
                )

        min_age = values.get("min_age", game.min_age)
        max_age = values.get("max_age", game.max_age)

        if min_age > max_age:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum age cannot be greater than maximum age.",
            )

        for key, value in values.items():
            setattr(game, key, value)

        return self.repository.save(game)

    def delete_game(self, game_id: int) -> None:
        game = self.get_game_or_404(game_id)
        self.repository.delete(game)
