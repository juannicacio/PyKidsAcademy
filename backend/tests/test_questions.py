import pytest
from fastapi import HTTPException

from app.models.challenge import Challenge
from app.models.game import Game
from app.models.level import Level
from app.services.question_service import QuestionService
from app.schemas.question import QuestionCreate, QuestionUpdate


def create_game(db):
    game = Game(
        title="Math",
        slug="math",
        category="Logic",
        difficulty=1,
        min_age=6,
        max_age=10,
        xp_reward=10,
        coin_reward=5,
        is_active=True,
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


def create_level(db, game):
    level = Level(
        game_id=game.id,
        title="Level 1",
        level_number=1,
        xp_reward=20,
        coin_reward=10,
        is_active=True,
    )
    db.add(level)
    db.commit()
    db.refresh(level)
    return level


def create_challenge(db, level):
    challenge = Challenge(
        level_id=level.id,
        title="Challenge 1",
        challenge_type="multiple_choice",
        challenge_order=1,
        xp_reward=30,
        coin_reward=15,
        is_active=True,
    )
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return challenge


@pytest.fixture
def service(db):
    return QuestionService(db)


@pytest.fixture
def challenge(db):
    game = create_game(db)
    level = create_level(db, game)
    return create_challenge(db, level)


def test_create_question(service, challenge):
    question = service.create(
        QuestionCreate(
            challenge_id=challenge.id,
            question_text="2 + 2 = ?",
            question_type="multiple_choice",
            question_order=1,
            explanation="Basic math",
            xp_reward=10,
            is_active=True,
        )
    )

    assert question.id is not None
    assert question.question_text == "2 + 2 = ?"


def test_get_question(service, challenge):
    question = service.create(
        QuestionCreate(
            challenge_id=challenge.id,
            question_text="Question",
            question_type="text",
            question_order=1,
            xp_reward=5,
            is_active=True,
        )
    )

    found = service.get(question.id)

    assert found.id == question.id


def test_list_questions(service, challenge):
    service.create(
        QuestionCreate(
            challenge_id=challenge.id,
            question_text="A",
            question_type="text",
            question_order=1,
            xp_reward=5,
            is_active=True,
        )
    )

    questions = service.list()

    assert len(questions) == 1


def test_list_questions_by_challenge(service, challenge):
    service.create(
        QuestionCreate(
            challenge_id=challenge.id,
            question_text="A",
            question_type="text",
            question_order=1,
            xp_reward=5,
            is_active=True,
        )
    )

    questions = service.list_by_challenge(challenge.id)

    assert len(questions) == 1


def test_list_active_questions(service, challenge):
    service.create(
        QuestionCreate(
            challenge_id=challenge.id,
            question_text="Active",
            question_type="text",
            question_order=1,
            xp_reward=5,
            is_active=True,
        )
    )

    service.create(
        QuestionCreate(
            challenge_id=challenge.id,
            question_text="Inactive",
            question_type="text",
            question_order=2,
            xp_reward=5,
            is_active=False,
        )
    )

    questions = service.list_active(challenge.id)

    assert len(questions) == 1
    assert questions[0].question_text == "Active"


def test_update_question(service, challenge):
    question = service.create(
        QuestionCreate(
            challenge_id=challenge.id,
            question_text="Old",
            question_type="text",
            question_order=1,
            xp_reward=5,
            is_active=True,
        )
    )

    updated = service.update(
        question.id,
        QuestionUpdate(question_text="New"),
    )

    assert updated.question_text == "New"


def test_delete_question(service, challenge):
    question = service.create(
        QuestionCreate(
            challenge_id=challenge.id,
            question_text="Delete",
            question_type="text",
            question_order=1,
            xp_reward=5,
            is_active=True,
        )
    )

    service.delete(question.id)

    with pytest.raises(HTTPException):
        service.get(question.id)


def test_challenge_not_found(service):
    with pytest.raises(HTTPException):
        service.create(
            QuestionCreate(
                challenge_id=999,
                question_text="Test",
                question_type="text",
                question_order=1,
                xp_reward=5,
                is_active=True,
            )
        )


def test_duplicate_question_order(service, challenge):
    service.create(
        QuestionCreate(
            challenge_id=challenge.id,
            question_text="One",
            question_type="text",
            question_order=1,
            xp_reward=5,
            is_active=True,
        )
    )

    with pytest.raises(HTTPException):
        service.create(
            QuestionCreate(
                challenge_id=challenge.id,
                question_text="Two",
                question_type="text",
                question_order=1,
                xp_reward=5,
                is_active=True,
            )
        )


def test_question_not_found(service):
    with pytest.raises(HTTPException):
        service.get(999)
