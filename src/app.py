from fastapi import FastAPI
from http import HTTPStatus

from src.schemas import Message,PublicUser

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Hello Word"}
