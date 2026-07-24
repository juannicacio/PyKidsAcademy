from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.student_achievement import (
    StudentAchievementCreate,
    StudentAchievementResponse,
)
from app.services.student_achievement_service import (
    StudentAchievementService,
)

router = APIRouter(
    prefix="/student-achievements",
    tags=["Student Achievements"],
)


@router.post(
    "/",
    response_model=StudentAchievementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student_achievement(
    data: StudentAchievementCreate,
    db: Session = Depends(get_db),
):
    service = StudentAchievementService(db)
    return service.create(data)


@router.get(
    "/",
    response_model=list[StudentAchievementResponse],
)
def list_student_achievements(
    db: Session = Depends(get_db),
):
    service = StudentAchievementService(db)
    return service.list_all()


@router.get(
    "/{student_achievement_id}",
    response_model=StudentAchievementResponse,
)
def get_student_achievement(
    student_achievement_id: int,
    db: Session = Depends(get_db),
):
    service = StudentAchievementService(db)
    return service.get(student_achievement_id)


@router.get(
    "/student/{student_id}",
    response_model=list[StudentAchievementResponse],
)
def list_student_achievements_by_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    service = StudentAchievementService(db)
    return service.list_by_student(student_id)


@router.delete(
    "/{student_achievement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_student_achievement(
    student_achievement_id: int,
    db: Session = Depends(get_db),
):
    service = StudentAchievementService(db)
    service.delete(student_achievement_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
