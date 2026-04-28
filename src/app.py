from fastapi import FastAPI, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas import Message, PublicUser, PrivateUser
from models import Users
from database import get_db

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Hello Word"}


@app.post("/create/", status_code=HTTPStatus.CREATED, response_model=PublicUser)
def create_user(user: PrivateUser, session: Session = Depends(get_db)):

    existing_user = session.scalar(
        select(Users).where(
            (Users.username == user.username) | (Users.email == user.email)
        )
    )

    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists",
            )
        elif existing_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already exists",
            )

    new_user = Users(username=user.username, age=user.age, email=user.email)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@app.get("/read/", status_code=HTTPStatus.OK)
def read_users(session: Session = Depends(get_db)):
    users = session.scalars(select(Users)).all()
    return users