from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
import pytest
from fastapi.testclient import TestClient

from sqlalchemy.pool import StaticPool
from models import Base, User
from app import app
from database import get_db
from schemas import PrivateUser
from security import get_password_hash, create_token, validaty_token
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    os.getenv("DATABASE_URL")
    )
SessionTest = sessionmaker(bind=engine)

@pytest.fixture
def session():
    with SessionTest() as session:
        yield session
        session.query(User).delete()
        session.commit()


@pytest.fixture
def client_override(session):
    def get_db_override():
        yield session

    def get_id_test_token():
        test_user = session.scalar(select(User).where(
            User.email == "test@example.com", User.username == "test"
            )
        )

        if test_user:
            yield test_user.id
        elif test_user is None:
            yield 0
        

    app.dependency_overrides[get_db] = get_db_override
    app.dependency_overrides[validaty_token] = get_id_test_token

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def add_user_database(session):
    new_user = User(
        username="test",
        age= 0,
        email= "test@example.com",
        password= get_password_hash("testtest")
    )

    session.add(new_user)
    session.commit  

    return new_user
