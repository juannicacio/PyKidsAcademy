from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentStatsUpdate,
    StudentUpdate,
)
from app.services.student_service import (
    create_student,
    delete_student,
    get_student_or_404,
    list_students,
    update_student,
    update_student_stats,
)

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_student(db, current_user, student)


@router.get(
    "",
    response_model=list[StudentResponse],
)
def list_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_students(db, current_user)


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
)
def get_one(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_student_or_404(
        db,
        current_user,
        student_id,
    )


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
)
def update(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_student(
        db,
        current_user,
        student_id,
        student,
    )

@router.put(
    "/{student_id}/stats",
    response_model=StudentResponse,
)
def update_stats(
    student_id: int,
    stats: StudentStatsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_student_stats(
        db,
        current_user,
        student_id,
        stats,
    )

@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_student(
        db,
        current_user,
        student_id,
    )
