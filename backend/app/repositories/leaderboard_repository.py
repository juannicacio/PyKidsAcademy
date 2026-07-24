from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.student import Student


class LeaderboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def by_xp(self):
        return (
            self.db.query(Student)
            .order_by(desc(Student.xp), Student.id)
            .all()
        )

    def by_coins(self):
        return (
            self.db.query(Student)
            .order_by(desc(Student.coins), Student.id)
            .all()
        )

    def by_level(self):
        return (
            self.db.query(Student)
            .order_by(desc(Student.learning_level), Student.id)
            .all()
        )
