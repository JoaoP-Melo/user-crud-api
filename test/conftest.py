from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker, Session
import pytest
from fastapi.testclient import TestClient

from sqlalchemy.pool import StaticPool
from models import Base, Users
from app import app
from database import get_db
from schemas import PrivateUser

@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def session(engine):
    SessionTest = sessionmaker(bind=engine)
    with SessionTest() as session:
        yield session


@pytest.fixture
def client_override(session):
    def get_db_override():
        yield session

    app.dependency_overrides[get_db] = get_db_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def add_user_database(session):
    new_user = Users(
        username="GhostUser",
        age= 0,
        email= "ghost_user@example.com"
    )

    session.add(new_user)
    session.commit  
    
    return new_user
