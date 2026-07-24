from sqlalchemy.orm import Session

from app.models.question import Question


class QuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, question: Question) -> Question:
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question

    def list_all(self) -> list[Question]:
        return (
            self.db.query(Question)
            .order_by(
                Question.challenge_id,
                Question.question_order,
            )
            .all()
        )

    def list_by_challenge(self, challenge_id: int) -> list[Question]:
        return (
            self.db.query(Question)
            .filter(Question.challenge_id == challenge_id)
            .order_by(Question.question_order)
            .all()
        )

    def list_active_by_challenge(self, challenge_id: int) -> list[Question]:
        return (
            self.db.query(Question)
            .filter(
                Question.challenge_id == challenge_id,
                Question.is_active.is_(True),
            )
            .order_by(Question.question_order)
            .all()
        )

    def get_by_id(self, question_id: int) -> Question | None:
        return (
            self.db.query(Question)
            .filter(Question.id == question_id)
            .first()
        )

    def get_by_challenge_and_order(
        self,
        challenge_id: int,
        question_order: int,
    ) -> Question | None:
        return (
            self.db.query(Question)
            .filter(
                Question.challenge_id == challenge_id,
                Question.question_order == question_order,
            )
            .first()
        )

    def save(self, question: Question) -> Question:
        self.db.commit()
        self.db.refresh(question)
        return question

    def delete(self, question: Question) -> None:
        self.db.delete(question)
        self.db.commit()
