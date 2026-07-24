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


def create_student(client, headers):
    response = client.post(
        "/students",
        headers=headers,
        json={
            "first_name": "Alice",
            "birth_month": 5,
            "birth_year": 2018,
            "avatar": None,
        },
    )

    assert response.status_code == 201
    return response.json()["id"]


def create_achievement(client):
    response = client.post(
        "/achievements",
        json=achievement_payload(),
    )

    assert response.status_code == 201
    return response.json()["id"]


def test_create_student_achievement(client, auth_headers):
    headers = auth_headers()

    student_id = create_student(client, headers)
    achievement_id = create_achievement(client)

    response = client.post(
        "/student-achievements",
        json={
            "student_id": student_id,
            "achievement_id": achievement_id,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["student_id"] == student_id
    assert data["achievement_id"] == achievement_id
    assert data["notified"] is False
    assert data["id"] > 0


def test_list_student_achievements(client, auth_headers):
    headers = auth_headers()

    student_id = create_student(client, headers)
    achievement_id = create_achievement(client)

    client.post(
        "/student-achievements",
        json={
            "student_id": student_id,
            "achievement_id": achievement_id,
        },
    )

    response = client.get("/student-achievements")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_student_achievement(client, auth_headers):
    headers = auth_headers()

    student_id = create_student(client, headers)
    achievement_id = create_achievement(client)

    create = client.post(
        "/student-achievements",
        json={
            "student_id": student_id,
            "achievement_id": achievement_id,
        },
    )

    sa_id = create.json()["id"]

    response = client.get(f"/student-achievements/{sa_id}")

    assert response.status_code == 200
    assert response.json()["id"] == sa_id


def test_delete_student_achievement(client, auth_headers):
    headers = auth_headers()

    student_id = create_student(client, headers)
    achievement_id = create_achievement(client)

    create = client.post(
        "/student-achievements",
        json={
            "student_id": student_id,
            "achievement_id": achievement_id,
        },
    )

    sa_id = create.json()["id"]

    response = client.delete(
        f"/student-achievements/{sa_id}"
    )

    assert response.status_code == 204

    response = client.get(
        f"/student-achievements/{sa_id}"
    )

    assert response.status_code == 404


def test_duplicate_student_achievement(client, auth_headers):
    headers = auth_headers()

    student_id = create_student(client, headers)
    achievement_id = create_achievement(client)

    payload = {
        "student_id": student_id,
        "achievement_id": achievement_id,
    }

    response = client.post(
        "/student-achievements",
        json=payload,
    )

    assert response.status_code == 201

    response = client.post(
        "/student-achievements",
        json=payload,
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": "Achievement already unlocked by this student."
    }
