from http import HTTPStatus
from fastapi.testclient import TestClient

from src.app import app
from src.schemas import PublicUser

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello Word"}
