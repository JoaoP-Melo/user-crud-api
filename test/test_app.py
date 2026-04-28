from http import HTTPStatus
from fastapi.testclient import TestClient
from sqlalchemy import select, func
from models import Users
from database import get_db
from app import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello Word"}


def test_create_user(client_override, session):
    response = client_override.post(
        "/create/", json={"username": "test", "age": 15, "email": "test@example.com"}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "test",
        "age": 15,
        "email": "test@example.com",
    }

    query = select(Users).where(
        Users.email == "test@example.com",
        Users.username == "test"
    )

    new_user = session.execute(query).scalars().first()

    assert new_user.username == "test"
    assert new_user.email == "test@example.com"


def test_read_users(session = get_db):
    response = client.get("/read/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() is not None
