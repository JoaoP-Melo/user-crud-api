from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from jwt import encode, decode

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from database import get_db
from models import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from http import HTTPStatus


SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = HTTPBearer()
pwd_context = PasswordHash.recommended()

def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def create_token(user_id: int):
    to_encode = {"sub": str(user_id)}

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded


def validaty_token(
        encoded_token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
        session : Session = Depends(get_db)
        ):
    
    credentials_exception = HTTPException(  
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(encoded_token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        subject_id = payload.get("sub")

        if not subject_id:
             raise HTTPException(  
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='id not found'
                )
    except:
        raise HTTPException(  
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Could not validate credentials'
                )
    
    
    existing_user = session.scalar(
        select(User).where(
           (User.id == int(subject_id))
        )
    )

    if not existing_user:
        raise HTTPException(  
                status_code=HTTPStatus.NOT_FOUND,
                detail='User not found'
                )
    
    return existing_user.id