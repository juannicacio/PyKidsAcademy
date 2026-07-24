def update_student(client, headers, student_id, xp, coins, learning_level):
    response = client.put(
        f"/students/{student_id}/stats",
        headers=headers,
        json={
            "xp": xp,
            "coins": coins,
            "learning_level": learning_level,
        },
    )

    assert response.status_code == 200

def create_student(client, headers, first_name):
    response = client.post(
        "/students",
        headers=headers,
        json={
            "first_name": first_name,
            "birth_month": 5,
            "birth_year": 2018,
            "avatar": None,
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_leaderboard_by_xp(client, auth_headers):
    headers = auth_headers()

    student_id = create_student(client, headers, "Alice")

    update_student(client, headers, student_id, 300, 20, 2)

    response = client.get("/leaderboard/xp")

    assert response.status_code == 200

    data = response.json()

    assert data[0]["first_name"] == "Alice"
    assert data[0]["xp"] == 300


def test_leaderboard_by_coins(client, auth_headers):
    headers = auth_headers()

    student_id = create_student(client, headers, "Alice")

    update_student(client, headers, student_id, 100, 75, 3)

    response = client.get("/leaderboard/coins")

    assert response.status_code == 200

    data = response.json()

    assert data[0]["coins"] == 75


def test_leaderboard_by_level(client, auth_headers):
    headers = auth_headers()

    student_id = create_student(client, headers, "Alice")

    update_student(client, headers, student_id, 100, 20, 5)

    response = client.get("/leaderboard/level")

    assert response.status_code == 200

    data = response.json()

    assert data[0]["learning_level"] == 5
