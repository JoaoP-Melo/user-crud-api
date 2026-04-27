from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str

class PublicUser(BaseModel):
    nome: str
    idade: int
    email: EmailStr


class PrivateUser(PublicUser):
    cpf: str
