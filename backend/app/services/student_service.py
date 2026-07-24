from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.user import User
from app.repositories.student_repository import StudentRepository
from app.schemas.student import (
    StudentCreate,
    StudentStatsUpdate,
    StudentUpdate,
)

def create_student(
    db: Session,
    user: User,
    data: StudentCreate,
) -> Student:

    repository = StudentRepository(db)

    total_students = repository.count_by_user(user.id)

    if total_students >= user.max_students:
        raise HTTPException(
            status_code=400,
            detail="Student limit reached.",
        )

    student = Student(
        user_id=user.id,
        first_name=data.first_name,
        birth_month=data.birth_month,
        birth_year=data.birth_year,
        avatar=data.avatar,
    )

    return repository.create(student)


def list_students(
    db: Session,
    user: User,
) -> list[Student]:

    repository = StudentRepository(db)

    return repository.list_by_user(user.id)


def get_student_or_404(
    db: Session,
    user: User,
    student_id: int,
) -> Student:

    repository = StudentRepository(db)

    student = repository.get_by_id(student_id)

    if student is None or student.user_id != user.id:
        raise HTTPException(
            status_code=404,
            detail="Student not found.",
        )

    return student


def update_student(
    db: Session,
    user: User,
    student_id: int,
    data: StudentUpdate,
) -> Student:

    repository = StudentRepository(db)

    student = get_student_or_404(
        db,
        user,
        student_id,
    )

    updates = data.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(student, key, value)

    return repository.save(student)


def delete_student(
    db: Session,
    user: User,
    student_id: int,
) -> None:

    repository = StudentRepository(db)

    student = get_student_or_404(
        db,
        user,
        student_id,
    )

    repository.delete(student)

def update_student_stats(
    db: Session,
    user: User,
    student_id: int,
    data: StudentStatsUpdate,
) -> Student:

    repository = StudentRepository(db)

    student = get_student_or_404(
        db,
        user,
        student_id,
    )

    return repository.update_stats(
        student=student,
        xp=data.xp,
        coins=data.coins,
        learning_level=data.learning_level,
    )
