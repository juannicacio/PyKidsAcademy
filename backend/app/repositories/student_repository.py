from sqlalchemy.orm import Session

from app.models.student import Student


class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        student: Student,
    ) -> Student:
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def list_by_user(
        self,
        user_id: int,
    ) -> list[Student]:
        return (
            self.db.query(Student)
            .filter(Student.user_id == user_id)
            .order_by(Student.id)
            .all()
        )

    def count_by_user(
        self,
        user_id: int,
    ) -> int:
        return (
            self.db.query(Student)
            .filter(Student.user_id == user_id)
            .count()
        )

    def get_by_id(
        self,
        student_id: int,
    ) -> Student | None:
        return (
            self.db.query(Student)
            .filter(Student.id == student_id)
            .first()
        )

    def save(
        self,
        student: Student,
    ) -> Student:
        self.db.commit()
        self.db.refresh(student)
        return student

    def delete(
        self,
        student: Student,
    ) -> None:
        self.db.delete(student)
        self.db.commit()

    def update_stats(
        self,
        student,
        xp: int,
        coins: int,
        learning_level: int,
    ):
        student.xp = xp
        student.coins = coins
        student.learning_level = learning_level

        self.db.commit()
        self.db.refresh(student)

        return student
