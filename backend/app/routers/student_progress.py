from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.student_progress import (
    StudentProgressCreate,
    StudentProgressResponse,
    StudentProgressUpdate,
)
from app.services.student_progress_service import (
    StudentProgressService,
)

router = APIRouter(
    prefix="/student-progress",
    tags=["Student Progress"],
)


@router.post(
    "",
    response_model=StudentProgressResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_progress(
    data: StudentProgressCreate,
    db: Session = Depends(get_db),
):
    service = StudentProgressService(db)
    return service.create_progress(data)


@router.get(
    "/student/{student_id}",
    response_model=list[StudentProgressResponse],
)
def list_progress(
    student_id: int,
    db: Session = Depends(get_db),
):
    service = StudentProgressService(db)
    return service.list_student_progress(student_id)


@router.get(
    "/student/{student_id}/level/{level_id}",
    response_model=StudentProgressResponse,
)
def get_progress(
    student_id: int,
    level_id: int,
    db: Session = Depends(get_db),
):
    service = StudentProgressService(db)
    return service.get_progress_or_404(
        student_id,
        level_id,
    )


@router.put(
    "/student/{student_id}/level/{level_id}",
    response_model=StudentProgressResponse,
)
def update_progress(
    student_id: int,
    level_id: int,
    data: StudentProgressUpdate,
    db: Session = Depends(get_db),
):
    service = StudentProgressService(db)
    return service.update_progress(
        student_id,
        level_id,
        data,
    )


@router.delete(
    "/student/{student_id}/level/{level_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_progress(
    student_id: int,
    level_id: int,
    db: Session = Depends(get_db),
):
    service = StudentProgressService(db)
    service.delete_progress(
        student_id,
        level_id,
    )
