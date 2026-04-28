from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class PrivateUser(BaseModel):
    username: str
    age: int
    email: EmailStr


class PublicUser(PrivateUser):
    id: int
