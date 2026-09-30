import os

os.environ["DATABASE_URL"] = "sqlite:///./test_pocketsmart.db"
os.environ["SECRET_KEY"] = "test-secret-key"

from unittest import SkipTest

try:
    from fastapi.testclient import TestClient  # type: ignore[import-not-found]
except ModuleNotFoundError as exc:
    raise SkipTest("FastAPI is not installed in this environment.") from exc

from app.database import Base, engine
from app.main import app


client = TestClient(app)


def setup_module():
    Base.metadata.create_all(bind=engine)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register():
    email = "test-user@example.com"

    response = client.post(
        "/register",
        data={
            "email": email,
            "password": "password123",
        },
        follow_redirects=False,
    )

    # 303 means successful registration.
    # 400 is also accepted when the test user already exists.
    assert response.status_code in [303, 400]


def test_home_requires_authentication():

    response = client.post(
        "/generate-home",
        json={
            "budget": 100000,
            "rooms": ["Living Room"],
            "style": "Modern",
            "items": {
                "lights": 2
            },
        },
    )

    assert response.status_code == 401


def test_startup():
    response = client.get("/startup")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"