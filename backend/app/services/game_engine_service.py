from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.student_repository import StudentRepository
from app.repositories.game_repository import GameRepository
from app.repositories.level_repository import LevelRepository
from app.repositories.student_progress_repository import StudentProgressRepository

from app.schemas.game_engine import (
    CompleteLevelRequest,
    CompleteLevelResponse,
)
from app.models.student import Student
from app.models.game import Game
from app.models.level import Level
from app.models.student_progress import StudentProgress
from app.services.reward_engine import RewardEngine


class GameEngineService:


    def __init__(self, db: Session):
        self.db = db

        self.student_repository = StudentRepository(db)
        self.game_repository = GameRepository(db)
        self.level_repository = LevelRepository(db)
        self.progress_repository = StudentProgressRepository(db)
        self.reward_engine = RewardEngine()

    def _get_student(
        self,
        student_id: int,
    ) -> Student:

        student = self.student_repository.get_by_id(student_id)

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found.",
            )

        return student

    def _get_game(
        self,
        game_id: int,
    ) -> Game:

        game = self.game_repository.get_by_id(game_id)

        if game is None:
            raise HTTPException(
                status_code=404,
                detail="Game not found.",
            )

        return game

    def _get_level(
        self,
        level_id: int,
    ) -> Level:

        level = self.level_repository.get_by_id(level_id)

        if level is None:
            raise HTTPException(
                status_code=404,
                detail="Level not found.",
            )

        return level

    def _get_progress(
        self,
        student_id: int,
        level_id: int,
    ) -> StudentProgress:

        progress = self.progress_repository.get(
            student_id,
            level_id,
        )

        if progress is None:
            raise HTTPException(
                status_code=404,
                detail="Progress not found.",
            )

        return progress

    def _update_progress(
        self,
        progress: StudentProgress,
        request: CompleteLevelRequest,
    ) -> None:

        progress.completed = True
        progress.score = max(
            progress.score,
            request.score,
        )
        progress.stars = max(
            progress.stars,
            request.stars,
        )
        progress.best_time = request.elapsed_time
        progress.attempts += 1
        progress.last_played_at = datetime.now(UTC)

    def _update_student(
        self,
        student: Student,
        game: Game,
        level: Level,
        xp: int,
        coins: int,
        stars: int,
    ) -> None:

        student.xp += xp
        student.coins += coins

        student.stars += stars
        student.completed_levels += 1

        student.learning_level = (
            self.reward_engine.calculate_learning_level(
                student.xp,
            )
        )

        student.current_game_id = game.id
        student.current_level_id = level.id

        student.current_streak += 1

        if student.current_streak > student.longest_streak:
            student.longest_streak = student.current_streak

        student.last_played_at = datetime.now(UTC)

    def _unlock_next_level(
        self,
        student: Student,
        game: Game,
        level: Level,
    ) -> bool:

        next_level = self.level_repository.get_next_level(
            game.id,
            level.level_number,
        )

        if next_level is None:
            return False

        next_progress = self.progress_repository.get(
            student.id,
            next_level.id,
        )

        if next_progress is None:

            next_progress = StudentProgress(
                student_id=student.id,
                level_id=next_level.id,
                completed=False,
                score=0,
                stars=0,
                attempts=0,
            )

            self.progress_repository.create(
                next_progress,
            )

        return True

    def complete_level(
        self,
        request: CompleteLevelRequest,
    ) -> CompleteLevelResponse:


        student = self._get_student(
            request.student_id,
        )

        game = self._get_game(
            request.game_id,
        )

        level = self._get_level(
            request.level_id,
        )

        progress = self._get_progress(
            request.student_id,
            request.level_id,
        )

        self._update_progress(
            progress,
            request,
        )

        xp, coins = self.reward_engine.calculate(
            request.stars,
        )

        self._update_student(
            student=student,
            game=game,
            level=level,
            xp=xp,
            coins=coins,
            stars=request.stars,
        )

        unlocked_next_level = self._unlock_next_level(
            student,
            game,
            level,
        )


        self.progress_repository.save(progress)
        self.student_repository.save(student)

        return CompleteLevelResponse(
            xp=xp,
            coins=coins,
            learning_level=student.learning_level,
            unlocked_next_level=unlocked_next_level,
            completed=True,
        )
