def test_auth_headers_fixture(client, auth_headers):
    headers = auth_headers()

    response = client.get(
        "/auth/me",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert "email" in data
    assert data["role"] == "parent"
