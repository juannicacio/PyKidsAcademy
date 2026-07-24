def test_create_student(client, auth_headers):
    headers = auth_headers()

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

    data = response.json()

    assert data["id"] > 0
    assert data["user_id"] > 0
    assert data["first_name"] == "Alice"
    assert data["birth_month"] == 5
    assert data["birth_year"] == 2018
    assert data["avatar"] is None
    assert data["learning_level"] == 1
    assert data["xp"] == 0
    assert data["coins"] == 0


def test_list_students(client, auth_headers):
    headers = auth_headers()

    create = client.post(
        "/students",
        headers=headers,
        json={
            "first_name": "Alice",
            "birth_month": 5,
            "birth_year": 2018,
            "avatar": None,
        },
    )

    assert create.status_code == 201

    response = client.get(
        "/students",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1

    student = data[0]

    assert student["id"] > 0
    assert student["user_id"] > 0
    assert student["first_name"] == "Alice"
    assert student["birth_month"] == 5
    assert student["birth_year"] == 2018
    assert student["avatar"] is None
    assert student["learning_level"] == 1
    assert student["xp"] == 0
    assert student["coins"] == 0


def test_get_student(client, auth_headers):
    headers = auth_headers()

    create = client.post(
        "/students",
        headers=headers,
        json={
            "first_name": "Alice",
            "birth_month": 5,
            "birth_year": 2018,
            "avatar": None,
        },
    )

    assert create.status_code == 201

    student_id = create.json()["id"]

    response = client.get(
        f"/students/{student_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student_id
    assert data["first_name"] == "Alice"
    assert data["birth_month"] == 5
    assert data["birth_year"] == 2018
    assert data["avatar"] is None
    assert data["learning_level"] == 1
    assert data["xp"] == 0
    assert data["coins"] == 0


def test_update_student(client, auth_headers):
    headers = auth_headers()

    create = client.post(
        "/students",
        headers=headers,
        json={
            "first_name": "Alice",
            "birth_month": 5,
            "birth_year": 2018,
            "avatar": None,
        },
    )

    assert create.status_code == 201

    student_id = create.json()["id"]

    response = client.put(
        f"/students/{student_id}",
        headers=headers,
        json={
            "first_name": "Emma",
            "birth_month": 7,
            "birth_year": 2019,
            "avatar": "cat.png",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student_id
    assert data["first_name"] == "Emma"
    assert data["birth_month"] == 7
    assert data["birth_year"] == 2019
    assert data["avatar"] == "cat.png"
    assert data["learning_level"] == 1
    assert data["xp"] == 0
    assert data["coins"] == 0


def test_delete_student(client, auth_headers):
    headers = auth_headers()

    create = client.post(
        "/students",
        headers=headers,
        json={
            "first_name": "Alice",
            "birth_month": 5,
            "birth_year": 2018,
            "avatar": None,
        },
    )

    assert create.status_code == 201

    student_id = create.json()["id"]

    response = client.delete(
        f"/students/{student_id}",
        headers=headers,
    )

    assert response.status_code == 204

    response = client.get(
        f"/students/{student_id}",
        headers=headers,
    )

    assert response.status_code == 404

def test_student_limit(client, auth_headers):
    headers = auth_headers()

    # Primer estudiante
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

    # Segundo estudiante
    response = client.post(
        "/students",
        headers=headers,
        json={
            "first_name": "Bob",
            "birth_month": 6,
            "birth_year": 2019,
            "avatar": None,
        },
    )

    assert response.status_code == 201

    # Tercer estudiante (debe fallar)
    response = client.post(
        "/students",
        headers=headers,
        json={
            "first_name": "Charlie",
            "birth_month": 7,
            "birth_year": 2020,
            "avatar": None,
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student limit reached."
    }
