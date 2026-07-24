from sqlalchemy.orm import Session

from fastapi import HTTPException
from app.models.student_achievement import StudentAchievement
from app.repositories.achievement_repository import AchievementRepository
from app.repositories.student_achievement_repository import (
    StudentAchievementRepository,
)
from app.repositories.student_repository import StudentRepository
from app.schemas.student_achievement import StudentAchievementCreate


class StudentAchievementService:
    def __init__(self, db: Session):
        self.db = db
        self.student_repository = StudentRepository(db)
        self.achievement_repository = AchievementRepository(db)
        self.student_achievement_repository = StudentAchievementRepository(db)

    def create(
        self,
        data: StudentAchievementCreate,
    ) -> StudentAchievement:
        student = self.student_repository.get_by_id(data.student_id)

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found.",
            )
        achievement = self.achievement_repository.get_by_id(
            data.achievement_id
        )

        if achievement is None:
            raise HTTPException(
                status_code=404,
                detail="Achievement not found.",
            )
        existing = (
            self.student_achievement_repository.get_by_student_and_achievement(
                data.student_id,
                data.achievement_id,
            )
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="Achievement already unlocked by this student.",
            )
        student_achievement = StudentAchievement(
            student_id=data.student_id,
            achievement_id=data.achievement_id,
        )

        return self.student_achievement_repository.create(
            student_achievement
        )

    def get(self, student_achievement_id: int) -> StudentAchievement:
        student_achievement = (
            self.student_achievement_repository.get_by_id(
                student_achievement_id
            )
        )

        if student_achievement is None:
            raise HTTPException(
                status_code=404,
                detail="Student achievement not found.",
            )
        return student_achievement

    def list_all(self) -> list[StudentAchievement]:
        return self.student_achievement_repository.list_all()

    def list_by_student(
        self,
        student_id: int,
    ) -> list[StudentAchievement]:
        return self.student_achievement_repository.list_by_student(
            student_id
        )

    def delete(self, student_achievement_id: int) -> None:
        student_achievement = (
            self.student_achievement_repository.get_by_id(
                student_achievement_id
            )
        )

        if student_achievement is None:
            raise HTTPException(
                status_code=404,
                detail="Student achievement not found.",
            )
        self.student_achievement_repository.delete(student_achievement)
