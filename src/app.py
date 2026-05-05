from fastapi import FastAPI, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from schemas import Message, PublicUser, PrivateUser
from models import User
from database import get_db
from security import get_password_hash

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Hello Word"}


@app.post("/create/", status_code=HTTPStatus.CREATED, response_model=PublicUser)
def create_user(user: PrivateUser, session: Session = Depends(get_db)):

    existing_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
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

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, age=user.age, email=user.email, password=hashed_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "age": new_user.age,
        "email": new_user.email,
    }


@app.get("/read/", status_code=HTTPStatus.OK)
def read_users(session: Session = Depends(get_db)):
    users = session.scalars(select(User)).all()
    return users


@app.put("/update/{id}", status_code=HTTPStatus.OK)
def update_users(id: int, user: PrivateUser, session: Session = Depends(get_db)):
    existing_user = session.scalar(
        select(User).where(
           (User.id == id)
        )
    )


    if existing_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ID not found",
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
    

    existing_user.username = user.username
    existing_user.age = user.age
    existing_user.email = user.email

    session.commit()
    
    return user


@app.get("/search/{id}", status_code=HTTPStatus.OK, response_model=PublicUser)
def search_user(id: int, session: Session = Depends(get_db)):
    existing_user = session.scalar(
        select(User).where(
           (User.id == id)
        )
    )

    if existing_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ID not found",
            )
    
    return existing_user


@app.delete("/delete/{id}", status_code=HTTPStatus.OK, response_model=PublicUser)
def delete_user(id: int, session: Session = Depends(get_db)):
    existing_user = session.scalar(
        select(User).where(
           (User.id == id)
        )
    )

    if existing_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ID not found",
            )
    
    session.delete(existing_user)
    session.commit()

    return existing_user