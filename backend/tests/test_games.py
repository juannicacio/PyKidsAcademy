def test_create_game(client):
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

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["title"] == "Math Adventure"
    assert data["slug"] == "math-adventure"
    assert data["category"] == "Math"
    assert data["difficulty"] == 1
    assert data["min_age"] == 5
    assert data["max_age"] == 8
    assert data["xp_reward"] == 20
    assert data["coin_reward"] == 10
    assert data["is_active"] is True


def test_list_games(client):
    client.post(
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

    response = client.get("/games")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Math Adventure"


def test_get_game(client):
    create = client.post(
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

    game_id = create.json()["id"]

    response = client.get(f"/games/{game_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == game_id
    assert data["title"] == "Math Adventure"


def test_update_game(client):
    create = client.post(
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

    game_id = create.json()["id"]

    response = client.put(
        f"/games/{game_id}",
        json={
            "title": "Reading Adventure",
            "difficulty": 2,
            "xp_reward": 30,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Reading Adventure"
    assert data["difficulty"] == 2
    assert data["xp_reward"] == 30


def test_delete_game(client):
    create = client.post(
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

    game_id = create.json()["id"]

    response = client.delete(f"/games/{game_id}")

    assert response.status_code == 204

    response = client.get(f"/games/{game_id}")

    assert response.status_code == 404


def test_duplicate_slug(client):
    payload = {
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
    }

    response = client.post("/games", json=payload)
    assert response.status_code == 201

    response = client.post("/games", json=payload)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Game slug already exists."
    }


def test_invalid_age_range(client):
    response = client.post(
        "/games",
        json={
            "title": "Math Adventure",
            "slug": "math-adventure",
            "description": "Learn math while playing.",
            "category": "Math",
            "difficulty": 1,
            "min_age": 10,
            "max_age": 5,
            "xp_reward": 20,
            "coin_reward": 10,
            "is_active": True,
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Minimum age cannot be greater than maximum age."
    }
