from datetime import datetime, UTC

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.student_progress import StudentProgress
from app.repositories.challenge_repository import ChallengeRepository
from app.repositories.game_repository import GameRepository
from app.repositories.level_repository import LevelRepository
from app.repositories.student_progress_repository import (
    StudentProgressRepository,
)
from app.repositories.student_repository import StudentRepository
from app.schemas.student_progress import (
    StudentProgressCreate,
    StudentProgressUpdate,
)


class StudentProgressService:

    def __init__(self, db: Session):
        self.progress_repository = StudentProgressRepository(db)
        self.student_repository = StudentRepository(db)
        self.game_repository = GameRepository(db)
        self.level_repository = LevelRepository(db)
        self.challenge_repository = ChallengeRepository(db)

    def create_progress(
        self,
        data: StudentProgressCreate,
    ) -> StudentProgress:

        if not self.student_repository.get_by_id(data.student_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found.",
            )

        if not self.game_repository.get_by_id(data.game_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found.",
            )

        if not self.level_repository.get_by_id(data.level_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Level not found.",
            )

        if (
            data.challenge_id is not None
            and not self.challenge_repository.get_by_id(
                data.challenge_id
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Challenge not found.",
            )

        if self.progress_repository.get(
            data.student_id,
            data.level_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Progress already exists.",
            )

        progress = StudentProgress(
            **data.model_dump(),
            last_played_at=datetime.now(UTC),
        )

        return self.progress_repository.create(progress)

    def list_student_progress(
        self,
        student_id: int,
    ):
        return self.progress_repository.list_by_student(student_id)

    def get_progress_or_404(
        self,
        student_id: int,
        level_id: int,
    ):
        progress = self.progress_repository.get(
            student_id,
            level_id,
        )

        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Progress not found.",
            )

        return progress

    def update_progress(
        self,
        student_id: int,
        level_id: int,
        data: StudentProgressUpdate,
    ):

        progress = self.get_progress_or_404(
            student_id,
            level_id,
        )

        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(progress, key, value)

        progress.last_played_at = datetime.now(UTC)

        return self.progress_repository.save(progress)

    def delete_progress(
        self,
        student_id: int,
        level_id: int,
    ):

        progress = self.get_progress_or_404(
            student_id,
            level_id,
        )

        self.progress_repository.delete(progress)
