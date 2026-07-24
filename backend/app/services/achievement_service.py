from sqlalchemy.orm import Session

from app.models.achievement import Achievement
from app.repositories.achievement_repository import AchievementRepository
from app.schemas.achievement import (
    AchievementCreate,
    AchievementUpdate,
)


class AchievementService:
    def __init__(self, db: Session):
        self.repository = AchievementRepository(db)

    def create(
        self,
        data: AchievementCreate,
    ) -> Achievement:

        if self.repository.get_by_slug(data.slug):
            raise ValueError("Achievement slug already exists.")

        achievement = Achievement(
            **data.model_dump()
        )

        return self.repository.create(achievement)

    def get_by_id(
        self,
        achievement_id: int,
    ) -> Achievement | None:
        return self.repository.get_by_id(
            achievement_id
        )

    def list_all(self) -> list[Achievement]:
        return self.repository.list_all()

    def list_active(self) -> list[Achievement]:
        return self.repository.list_active()

    def update(
        self,
        achievement: Achievement,
        data: AchievementUpdate,
    ) -> Achievement:

        values = data.model_dump(exclude_unset=True)

        if (
            "slug" in values
            and values["slug"] != achievement.slug
        ):
            existing = self.repository.get_by_slug(
                values["slug"]
            )

            if existing:
                raise ValueError(
                    "Achievement slug already exists."
                )

        for key, value in values.items():
            setattr(
                achievement,
                key,
                value,
            )

        return self.repository.save(
            achievement
        )

    def delete(
        self,
        achievement: Achievement,
    ) -> None:
        self.repository.delete(
            achievement
        )
