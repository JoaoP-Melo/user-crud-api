from fastapi import FastAPI, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from schemas import Message,PublicUser, PrivateUser
from models import Users
from database import get_db
app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Hello Word"}


@app.post("/create/")
def create_user(user: PrivateUser, session: Session = Depends(get_db)):
    query = (select(Users).
            where(
                or_(
                    Users.nome == user.nome,
                    Users.email == user.email,
                    Users.cpf == user.cpf)
            )
        )
    
    result = session.scalar(query)

    if result:
        if result.nome == user.nome:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif result.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )
        elif result.cpf == user.cpf:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='cpf already exists',
            )

    new_user = Users(**user.dict())

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user
