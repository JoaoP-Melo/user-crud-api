from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from jwt import encode

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTES = 30

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