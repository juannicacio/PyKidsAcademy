def create_game(client):
    response = client.post(
        "/games",
        json={
            "title": "Math Adventure",
            "slug": "math-adventure",
            "description": "Learn math while playing.",
            "category": "Math",
            "difficulty": 1,
            "min_age": 5,
            "max_age": 8,
            "xp_reward": 20,
            "coin_reward": 10,
            "is_active": True,
        },
    )

    return response.json()["id"]


def test_create_level(client):
    game_id = create_game(client)

    response = client.post(
        "/levels",
        json={
            "game_id": game_id,
            "title": "Level 1",
            "description": "Introduction",
            "level_number": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["game_id"] == game_id
    assert data["title"] == "Level 1"
    assert data["level_number"] == 1


def test_list_levels(client):
    game_id = create_game(client)

    client.post(
        "/levels",
        json={
            "game_id": game_id,
            "title": "Level 1",
            "description": "Introduction",
            "level_number": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    response = client.get("/levels")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Level 1"


def test_list_levels_by_game(client):
    game_id = create_game(client)

    client.post(
        "/levels",
        json={
            "game_id": game_id,
            "title": "Level 1",
            "description": "Introduction",
            "level_number": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    response = client.get(f"/levels/game/{game_id}")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["game_id"] == game_id


def test_list_active_levels_by_game(client):
    game_id = create_game(client)

    client.post(
        "/levels",
        json={
            "game_id": game_id,
            "title": "Level 1",
            "description": "Introduction",
            "level_number": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    client.post(
        "/levels",
        json={
            "game_id": game_id,
            "title": "Level 2",
            "description": "Hidden",
            "level_number": 2,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": False,
        },
    )

    response = client.get(f"/levels/game/{game_id}/active")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Level 1"


def test_get_level(client):
    game_id = create_game(client)

    create = client.post(
        "/levels",
        json={
            "game_id": game_id,
            "title": "Level 1",
            "description": "Introduction",
            "level_number": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    level_id = create.json()["id"]

    response = client.get(f"/levels/{level_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == level_id
    assert data["title"] == "Level 1"


def test_update_level(client):
    game_id = create_game(client)

    create = client.post(
        "/levels",
        json={
            "game_id": game_id,
            "title": "Level 1",
            "description": "Introduction",
            "level_number": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    level_id = create.json()["id"]

    response = client.put(
        f"/levels/{level_id}",
        json={
            "title": "Updated Level",
            "xp_reward": 30,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated Level"
    assert data["xp_reward"] == 30


def test_delete_level(client):
    game_id = create_game(client)

    create = client.post(
        "/levels",
        json={
            "game_id": game_id,
            "title": "Level 1",
            "description": "Introduction",
            "level_number": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    level_id = create.json()["id"]

    response = client.delete(f"/levels/{level_id}")

    assert response.status_code == 204

    response = client.get(f"/levels/{level_id}")

    assert response.status_code == 404


def test_create_level_with_invalid_game(client):
    response = client.post(
        "/levels",
        json={
            "game_id": 9999,
            "title": "Level 1",
            "description": "Introduction",
            "level_number": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Game not found."
    }


def test_duplicate_level_number_same_game(client):
    game_id = create_game(client)

    payload = {
        "game_id": game_id,
        "title": "Level 1",
        "description": "Introduction",
        "level_number": 1,
        "xp_reward": 10,
        "coin_reward": 5,
        "is_active": True,
    }

    response = client.post("/levels", json=payload)

    assert response.status_code == 201

    response = client.post("/levels", json=payload)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Level number already exists for this game."
    }


def test_same_level_number_different_games(client):
    game1 = create_game(client)

    client.post(
        "/levels",
        json={
            "game_id": game1,
            "title": "Level 1",
            "description": "Introduction",
            "level_number": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    response = client.post(
        "/games",
        json={
            "title": "Reading Adventure",
            "slug": "reading-adventure",
            "description": "Reading game",
            "category": "Reading",
            "difficulty": 1,
            "min_age": 5,
            "max_age": 8,
            "xp_reward": 20,
            "coin_reward": 10,
            "is_active": True,
        },
    )

    game2 = response.json()["id"]

    response = client.post(
        "/levels",
        json={
            "game_id": game2,
            "title": "Level 1",
            "description": "Introduction",
            "level_number": 1,
            "xp_reward": 10,
            "coin_reward": 5,
            "is_active": True,
        },
    )

    assert response.status_code == 201
