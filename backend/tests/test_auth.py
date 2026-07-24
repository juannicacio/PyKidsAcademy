def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "Password123!",
            "country": "US",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] > 0
    assert data["email"] == "test@example.com"
    assert data["country"] == "US"
    assert data["role"] == "parent"
    assert data["is_active"] is True


def test_register_duplicate_email(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "Password123!",
        "country": "US",
    }

    first = client.post(
        "/auth/register",
        json=payload,
    )

    assert first.status_code == 200

    second = client.post(
        "/auth/register",
        json=payload,
    )

    assert second.status_code == 400

    data = second.json()

    assert data["detail"] == "Email already registered."

def test_login_user(client):
    payload = {
        "email": "login@example.com",
        "password": "Password123!",
        "country": "US",
    }

    register = client.post(
        "/auth/register",
        json=payload,
    )

    assert register.status_code == 200

    response = client.post(
        "/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["access_token"] != ""
    assert data["token_type"] == "bearer"

def test_get_current_user(client):
    payload = {
        "email": "me@example.com",
        "password": "Password123!",
        "country": "US",
    }

    register = client.post(
        "/auth/register",
        json=payload,
    )

    assert register.status_code == 200

    login = client.post(
        "/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == payload["email"]
    assert data["country"] == payload["country"]
    assert data["role"] == "parent"
    assert data["is_active"] is True
