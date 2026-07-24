from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.question import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
)
from app.services.question_service import QuestionService

router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.post(
    "",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
):
    return QuestionService(db).create(question)


@router.get(
    "",
    response_model=List[QuestionResponse],
)
def list_questions(
    db: Session = Depends(get_db),
):
    return QuestionService(db).list()


@router.get(
    "/{question_id}",
    response_model=QuestionResponse,
)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
):
    return QuestionService(db).get(question_id)


@router.get(
    "/challenge/{challenge_id}",
    response_model=List[QuestionResponse],
)
def list_questions_by_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
):
    return QuestionService(db).list_by_challenge(challenge_id)


@router.get(
    "/challenge/{challenge_id}/active",
    response_model=List[QuestionResponse],
)
def list_active_questions(
    challenge_id: int,
    db: Session = Depends(get_db),
):
    return QuestionService(db).list_active(challenge_id)


@router.put(
    "/{question_id}",
    response_model=QuestionResponse,
)
def update_question(
    question_id: int,
    question: QuestionUpdate,
    db: Session = Depends(get_db),
):
    return QuestionService(db).update(question_id, question)


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
):
    QuestionService(db).delete(question_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
