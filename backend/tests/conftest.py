import os
import uuid

os.environ["ENV_FILE"] = ".env.test"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings


engine = create_engine(settings.DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

import uuid

import pytest


@pytest.fixture
def auth_headers(client):
    def _auth_headers():
        email = f"{uuid.uuid4()}@example.com"

        payload = {
            "email": email,
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

        return {
            "Authorization": f"Bearer {token}",
        }

    return _auth_headers
