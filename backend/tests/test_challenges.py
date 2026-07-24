from app.models.challenge import Challenge
from app.models.game import Game
from app.models.level import Level


def create_game(db):
    game = Game(
        title="Math",
        slug="math",
        description="Math Game",
        category="math",
        difficulty=1,
        min_age=5,
        max_age=8,
        xp_reward=50,
        coin_reward=10,
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
        description="First level",
        level_number=1,
        xp_reward=20,
        coin_reward=5,
        is_active=True,
    )
    db.add(level)
    db.commit()
    db.refresh(level)
    return level


def create_challenge(db, level):
    challenge = Challenge(
        level_id=level.id,
        title="Addition",
        description="2 + 2",
        challenge_type="multiple_choice",
        challenge_order=1,
        xp_reward=10,
        coin_reward=5,
        is_active=True,
    )
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return challenge


def test_create_challenge(client, db):
    game = create_game(db)
    level = create_level(db, game)

    response = client.post(
        "/challenges",
        json={
            "level_id": level.id,
            "title": "Addition",
            "description": "2 + 2",
            "challenge_type": "multiple_choice",
            "challenge_order": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Addition"
    assert data["level_id"] == level.id


def test_get_challenge(client, db):
    game = create_game(db)
    level = create_level(db, game)
    challenge = create_challenge(db, level)

    response = client.get(f"/challenges/{challenge.id}")

    assert response.status_code == 200
    assert response.json()["id"] == challenge.id


def test_list_challenges(client, db):
    game = create_game(db)
    level = create_level(db, game)
    create_challenge(db, level)

    response = client.get("/challenges")

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_list_challenges_by_level(client, db):
    game = create_game(db)
    level = create_level(db, game)
    create_challenge(db, level)

    response = client.get(f"/challenges/level/{level.id}")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_active_challenges(client, db):
    game = create_game(db)
    level = create_level(db, game)
    create_challenge(db, level)

    response = client.get(f"/challenges/level/{level.id}/active")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_challenge(client, db):
    game = create_game(db)
    level = create_level(db, game)
    challenge = create_challenge(db, level)

    response = client.put(
        f"/challenges/{challenge.id}",
        json={
            "title": "Updated Challenge",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Challenge"


def test_delete_challenge(client, db):
    game = create_game(db)
    level = create_level(db, game)
    challenge = create_challenge(db, level)

    response = client.delete(f"/challenges/{challenge.id}")

    assert response.status_code == 204


def test_create_invalid_level(client):
    response = client.post(
        "/challenges",
        json={
            "level_id": 99999,
            "title": "Invalid",
            "description": "",
            "challenge_type": "multiple_choice",
            "challenge_order": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    assert response.status_code == 404


def test_duplicate_order(client, db):
    game = create_game(db)
    level = create_level(db, game)

    create_challenge(db, level)

    response = client.post(
        "/challenges",
        json={
            "level_id": level.id,
            "title": "Duplicate",
            "description": "",
            "challenge_type": "multiple_choice",
            "challenge_order": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    assert response.status_code == 400


def test_get_missing_challenge(client):
    response = client.get("/challenges/99999")

    assert response.status_code == 404
