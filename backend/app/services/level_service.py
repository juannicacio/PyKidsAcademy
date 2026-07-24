from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.level import Level
from app.repositories.game_repository import GameRepository
from app.repositories.level_repository import LevelRepository
from app.schemas.level import LevelCreate, LevelUpdate


class LevelService:
    def __init__(self, db: Session):
        self.level_repository = LevelRepository(db)
        self.game_repository = GameRepository(db)

    def create_level(self, data: LevelCreate) -> Level:
        game = self.game_repository.get_by_id(data.game_id)

        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found.",
            )

        if self.level_repository.get_by_game_and_number(
            data.game_id,
            data.level_number,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Level number already exists for this game.",
            )

        level = Level(**data.model_dump())

        return self.level_repository.create(level)

    def list_levels(self) -> list[Level]:
        return self.level_repository.list_all()

    def list_levels_by_game(self, game_id: int) -> list[Level]:
        return self.level_repository.list_by_game(game_id)

    def list_active_levels_by_game(self, game_id: int) -> list[Level]:
        return self.level_repository.list_active_by_game(game_id)

    def get_level_or_404(self, level_id: int) -> Level:
        level = self.level_repository.get_by_id(level_id)

        if not level:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Level not found.",
            )

        return level

    def update_level(
        self,
        level_id: int,
        data: LevelUpdate,
    ) -> Level:
        level = self.get_level_or_404(level_id)

        values = data.model_dump(exclude_unset=True)

        if "level_number" in values:
            existing = self.level_repository.get_by_game_and_number(
                level.game_id,
                values["level_number"],
            )

            if existing and existing.id != level.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Level number already exists for this game.",
                )

        for key, value in values.items():
            setattr(level, key, value)

        return self.level_repository.save(level)

    def delete_level(self, level_id: int) -> None:
        level = self.get_level_or_404(level_id)
        self.level_repository.delete(level)
