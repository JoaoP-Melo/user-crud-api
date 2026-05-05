from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class PrivateUser(BaseModel):
    username: str
    age: int
    email: EmailStr
    password: str


class PublicUser(BaseModel):
    id: int
    username: str
    age: int
    email: EmailStr

