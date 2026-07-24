from sqlalchemy.orm import Session

from app.models.achievement import Achievement


class AchievementRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, achievement: Achievement) -> Achievement:
        self.db.add(achievement)
        self.db.commit()
        self.db.refresh(achievement)
        return achievement

    def get_by_id(self, achievement_id: int) -> Achievement | None:
        return (
            self.db.query(Achievement)
            .filter(Achievement.id == achievement_id)
            .first()
        )

    def get_by_slug(self, slug: str) -> Achievement | None:
        return (
            self.db.query(Achievement)
            .filter(Achievement.slug == slug)
            .first()
        )

    def list_all(self) -> list[Achievement]:
        return (
            self.db.query(Achievement)
            .order_by(Achievement.id)
            .all()
        )

    def list_active(self) -> list[Achievement]:
        return (
            self.db.query(Achievement)
            .filter(Achievement.active.is_(True))
            .order_by(Achievement.id)
            .all()
        )

    def save(self, achievement: Achievement) -> Achievement:
        self.db.commit()
        self.db.refresh(achievement)
        return achievement

    def delete(self, achievement: Achievement) -> None:
        self.db.delete(achievement)
        self.db.commit()
