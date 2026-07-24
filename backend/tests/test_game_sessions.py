from fastapi.testclient import TestClient
import uuid

def game_session_payload(student_id: int, game_id: int, level_id: int):
    return {
        "student_id": student_id,
        "game_id": game_id,
        "level_id": level_id,
    }


def create_user(client):
    email = f"{uuid.uuid4()}@example.com"

    payload = {
        "email": email,
        "password": "Password123!",
        "country": "US",
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200

    login = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "Password123!",
        },
    )

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


def create_student(client, headers):
    response = client.post(
        "/students",
        json={
            "first_name": "Mia",
            "birth_month": 6,
            "birth_year": 2019,
        },
        headers=headers,
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_game(client):
    response = client.post(
        "/games",
        json={
            "title": "Python Basics",
            "slug": f"python-{uuid.uuid4().hex[:8]}",
            "description": "Game",
            "category": "python",
            "difficulty": 1,
            "min_age": 4,
            "max_age": 8,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    assert response.status_code == 201

    return response.json()["id"]

def create_level(client, game_id):
    response = client.post(
        "/levels",
        json={
            "game_id": game_id,
            "title": "Level 1",
            "description": "First level",
            "level_number": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    assert response.status_code == 201

    return response.json()["id"]

def test_create_game_session(client):
    headers = create_user(client)

    student_id = create_student(client, headers)
    game_id = create_game(client)
    level_id = create_level(client, game_id)

    response = client.post(
        "/game-sessions",
        json=game_session_payload(
            student_id,
            game_id,
            level_id,
        ),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["student_id"] == student_id
    assert data["game_id"] == game_id
    assert data["level_id"] == level_id
    assert data["completed"] is False

def test_list_game_sessions(client):
    headers = create_user(client)

    student_id = create_student(client, headers)
    game_id = create_game(client)
    level_id = create_level(client, game_id)

    client.post(
        "/game-sessions",
        json=game_session_payload(
            student_id,
            game_id,
            level_id,
        ),
    )

    response = client.get("/game-sessions")

    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_game_session(client):
    headers = create_user(client)

    student_id = create_student(client, headers)
    game_id = create_game(client)
    level_id = create_level(client, game_id)

    created = client.post(
        "/game-sessions",
        json=game_session_payload(
            student_id,
            game_id,
            level_id,
        ),
    )

    session_id = created.json()["id"]

    response = client.get(f"/game-sessions/{session_id}")

    assert response.status_code == 200
    assert response.json()["id"] == session_id

def test_finish_game_session(client):
    headers = create_user(client)

    student_id = create_student(client, headers)
    game_id = create_game(client)
    level_id = create_level(client, game_id)

    created = client.post(
        "/game-sessions",
        json=game_session_payload(
            student_id,
            game_id,
            level_id,
        ),
    )

    session_id = created.json()["id"]

    response = client.put(
        f"/game-sessions/{session_id}/finish",
        json={
            "score": 100,
            "correct_answers": 10,
            "wrong_answers": 2,
            "xp_earned": 50,
            "coins_earned": 20,
            "completed": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["completed"] is True
    assert data["score"] == 100

def test_delete_game_session(client):
    headers = create_user(client)

    student_id = create_student(client, headers)
    game_id = create_game(client)
    level_id = create_level(client, game_id)

    created = client.post(
        "/game-sessions",
        json=game_session_payload(
            student_id,
            game_id,
            level_id,
        ),
    )

    session_id = created.json()["id"]

    response = client.delete(f"/game-sessions/{session_id}")

    assert response.status_code == 204

    response = client.get(f"/game-sessions/{session_id}")

    assert response.status_code == 404
