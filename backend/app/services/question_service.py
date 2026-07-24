from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.challenge import Challenge
from app.models.question import Question
from app.repositories.question_repository import QuestionRepository
from app.schemas.question import QuestionCreate, QuestionUpdate

class QuestionService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = QuestionRepository(db)

    def create(self, data: QuestionCreate) -> Question:
        challenge = (
            self.db.query(Challenge)
            .filter(Challenge.id == data.challenge_id)
            .first()
        )

        if challenge is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Challenge not found",
            )

        existing = self.repository.get_by_challenge_and_order(
            data.challenge_id,
            data.question_order,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question order already exists",
            )

        question = Question(**data.model_dump())

        return self.repository.create(question)

    def list(self) -> List[Question]:
        return self.repository.list_all()


    def list_by_challenge(self, challenge_id: int) -> List[Question]:
        return self.repository.list_by_challenge(challenge_id)


    def list_active(self, challenge_id: int) -> List[Question]:
        return self.repository.list_active_by_challenge(challenge_id)

    def get(self, question_id: int) -> Question:
        question = self.repository.get_by_id(question_id)

        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )

        return question

    def update(
        self,
        question_id: int,
        data: QuestionUpdate,
    ) -> Question:
        question = self.get(question_id)

        values = data.model_dump(exclude_unset=True)

        if "question_order" in values:
            existing = self.repository.get_by_challenge_and_order(
                question.challenge_id,
                values["question_order"],
            )

            if existing and existing.id != question.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Question order already exists",
                )

        for field, value in values.items():
            setattr(question, field, value)

        return self.repository.save(question)

    def delete(self, question_id: int) -> None:
        question = self.get(question_id)
        self.repository.delete(question)
