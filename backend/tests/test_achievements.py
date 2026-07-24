def achievement_payload():
    return {
        "name": "First Steps",
        "slug": "first-steps",
        "description": "Complete your first level.",
        "icon": "⭐",
        "category": "Progress",
        "xp_reward": 25,
        "coin_reward": 10,
        "active": True,
    }


def test_create_achievement(client):
    response = client.post(
        "/achievements",
        json=achievement_payload(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["name"] == "First Steps"
    assert data["slug"] == "first-steps"
    assert data["xp_reward"] == 25
    assert data["coin_reward"] == 10
    assert data["active"] is True


def test_list_achievements(client):
    client.post(
        "/achievements",
        json=achievement_payload(),
    )

    response = client.get("/achievements")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "First Steps"


def test_list_active_achievements(client):
    client.post(
        "/achievements",
        json=achievement_payload(),
    )

    inactive = achievement_payload()
    inactive["slug"] = "hidden"
    inactive["name"] = "Hidden"
    inactive["active"] = False

    client.post(
        "/achievements",
        json=inactive,
    )

    response = client.get("/achievements/active")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "First Steps"


def test_get_achievement(client):
    create = client.post(
        "/achievements",
        json=achievement_payload(),
    )

    achievement_id = create.json()["id"]

    response = client.get(
        f"/achievements/{achievement_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == achievement_id
    assert data["slug"] == "first-steps"


def test_update_achievement(client):
    create = client.post(
        "/achievements",
        json=achievement_payload(),
    )

    achievement_id = create.json()["id"]

    response = client.put(
        f"/achievements/{achievement_id}",
        json={
            "name": "Explorer",
            "xp_reward": 100,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Explorer"
    assert data["xp_reward"] == 100


def test_delete_achievement(client):
    create = client.post(
        "/achievements",
        json=achievement_payload(),
    )

    achievement_id = create.json()["id"]

    response = client.delete(
        f"/achievements/{achievement_id}"
    )

    assert response.status_code == 204

    response = client.get(
        f"/achievements/{achievement_id}"
    )

    assert response.status_code == 404


def test_duplicate_slug(client):
    payload = achievement_payload()

    response = client.post(
        "/achievements",
        json=payload,
    )

    assert response.status_code == 201

    response = client.post(
        "/achievements",
        json=payload,
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Achievement slug already exists."
    }


def test_get_missing_achievement(client):
    response = client.get("/achievements/9999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Achievement not found."
    }
