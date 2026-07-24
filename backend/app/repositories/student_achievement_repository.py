from sqlalchemy.orm import Session

from app.models.student_achievement import StudentAchievement


class StudentAchievementRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, student_achievement: StudentAchievement) -> StudentAchievement:
        self.db.add(student_achievement)
        self.db.commit()
        self.db.refresh(student_achievement)
        return student_achievement

    def get_by_id(self, student_achievement_id: int) -> StudentAchievement | None:
        return (
            self.db.query(StudentAchievement)
            .filter(StudentAchievement.id == student_achievement_id)
            .first()
        )

    def list_all(self) -> list[StudentAchievement]:
        return (
            self.db.query(StudentAchievement)
            .order_by(StudentAchievement.unlocked_at.desc())
            .all()
        )

    def list_by_student(self, student_id: int) -> list[StudentAchievement]:
        return (
            self.db.query(StudentAchievement)
            .filter(StudentAchievement.student_id == student_id)
            .order_by(StudentAchievement.unlocked_at.desc())
            .all()
        )

    def get_by_student_and_achievement(
        self,
        student_id: int,
        achievement_id: int,
    ) -> StudentAchievement | None:
        return (
            self.db.query(StudentAchievement)
            .filter(
                StudentAchievement.student_id == student_id,
                StudentAchievement.achievement_id == achievement_id,
            )
            .first()
        )

    def delete(self, student_achievement: StudentAchievement) -> None:
        self.db.delete(student_achievement)
        self.db.commit()
