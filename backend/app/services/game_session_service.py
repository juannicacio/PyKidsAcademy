from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.game import Game
from app.models.level import Level
from app.repositories.game_session_repository import GameSessionRepository
from app.schemas.game_session import (
    GameSessionCreate,
    GameSessionUpdate,
)


class GameSessionService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = GameSessionRepository(db)

    def create(self, data: GameSessionCreate):
        student = self.db.get(Student, data.student_id)
        if student is None:
            raise HTTPException(404, "Student not found")

        game = self.db.get(Game, data.game_id)
        if game is None:
            raise HTTPException(404, "Game not found")

        level = self.db.get(Level, data.level_id)
        if level is None:
            raise HTTPException(404, "Level not found")

        return self.repository.create(data)

    def get(self, session_id: int):
        session = self.repository.get_by_id(session_id)

        if session is None:
            raise HTTPException(404, "Game session not found")

        return session

    def list_all(self):
        return self.repository.list_all()

    def list_by_student(self, student_id: int):
        return self.repository.list_by_student(student_id)

    def finish(
        self,
        session_id: int,
        data: GameSessionUpdate,
    ):
        session = self.repository.get_by_id(session_id)

        if session is None:
            raise HTTPException(404, "Game session not found")

        return self.repository.finish(session, data)

    def delete(self, session_id: int):
        session = self.repository.get_by_id(session_id)

        if session is None:
            raise HTTPException(404, "Game session not found")

        self.repository.delete(session)
