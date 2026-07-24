from sqlalchemy.orm import Session

from app.models.student_progress import StudentProgress


class StudentProgressRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        progress: StudentProgress,
    ) -> StudentProgress:
        self.db.add(progress)
        self.db.commit()
        self.db.refresh(progress)
        return progress

    def list_by_student(
        self,
        student_id: int,
    ) -> list[StudentProgress]:
        return (
            self.db.query(StudentProgress)
            .filter(StudentProgress.student_id == student_id)
            .order_by(StudentProgress.level_id.asc())
            .all()
        )

    def get(
        self,
        student_id: int,
        level_id: int,
    ) -> StudentProgress | None:
        return (
            self.db.query(StudentProgress)
            .filter(
                StudentProgress.student_id == student_id,
                StudentProgress.level_id == level_id,
            )
            .first()
        )

    def save(
        self,
        progress: StudentProgress,
    ) -> StudentProgress:
        self.db.commit()
        self.db.refresh(progress)
        return progress

    def delete(
        self,
        progress: StudentProgress,
    ):
        self.db.delete(progress)
        self.db.commit()
