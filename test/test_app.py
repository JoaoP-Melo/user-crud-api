from http import HTTPStatus
from fastapi.testclient import TestClient
from sqlalchemy import select, func
from models import User
from database import get_db
from app import app

client = TestClient(app)


def test_read_root_sucess():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello Word"}


def test_create_user_success(client_override, session):
    response = client_override.post(
        "/create/", json={"username": "test", "age": 15, "email": "test@example.com", "password": "testtest"}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "test",
        "age": 15,
        "email": "test@example.com",
        "password": "testtest"
    }

    query = select(User).where(
        User.email == "test@example.com", User.username == "test"
    )

    new_user = session.execute(query).scalars().first()

    assert new_user.username == "test"
    assert new_user.email == "test@example.com"


def test_create_user_name_error(client_override, add_user_database, session):
    response = client_override.post(
        "/create/", json={"username": "GhostUser", "age": 15, "email": "test@example.com"}
    )

    assert response.status_code == HTTPStatus.CONFLICT

def test_create_user_email_error(client_override, add_user_database, session):
    response = client_override.post(
        "/create/", json={"username": "teste", "age": 15, "email": "ghost_user@example.com"}
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_read_users(session=get_db):
    response = client.get("/read/")
    assert response.status_code == HTTPStatus.OK


def test_update_users(client_override, add_user_database, session):
    existing_user = session.scalar(
        select(User).where(
           (User.id == 1)
        )
    )

    response = client_override.put(
        "/update/1", json={"username": "teste", "age": 0, "email": "teste@example.com"}
    )

    assert response.status_code == HTTPStatus.OK


def test_update_users_id_error(client_override, add_user_database, session):
    existing_user = session.scalar(
        select(User).where(
           (User.id == 1)
        )
    )

    response = client_override.put(
        "/update/0", json={"username": "teste", "age": 0, "email": "teste@example.com"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_users_email_error(client_override, add_user_database, session):
    existing_user = session.scalar(
        select(User).where(
           (User.id == 1)
        )
    )

    response = client_override.put(
        "/update/1", json={"username": "teste", "age": 0, "email": "ghost_user@example.com"}
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_update_users_name_error(client_override, add_user_database, session):
    existing_user = session.scalar(
        select(User).where(
           (User.id == 1)
        )
    )

    response = client_override.put(
        "/update/1", json={"username": "GhostUser", "age": 0, "email": "teste@example.com"}
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_search_users_success(client_override, add_user_database, session):
    existing_user = session.scalar(
        select(User).where(
           (User.id == 1)
        )
    )

    response = client_override.get(
       f"/search/{existing_user.id}"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == existing_user.username


def test_search_users_id_error(client_override, add_user_database, session):
    response = client_override.get(
       "/search/0"
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_success(client_override, add_user_database, session):
    existing_user = session.scalar(
        select(User).where(
           (User.id == 1)
        )
    )

    response = client_override.delete(
        f"/delete/{existing_user.id}"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == existing_user.username


def test_delete_user_id_error(client_override, add_user_database, session):
    response = client_override.delete(
        "/delete/0"
    )

    assert response.status_code == HTTPStatus.NOT_FOUND