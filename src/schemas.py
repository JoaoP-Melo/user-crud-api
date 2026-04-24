from pydantic import BaseModel


class Message(BaseModel):
    message: str


class PublicUser(BaseModel):
    id: int
    nome: str
    idade: int
    estado: str


class PrivateUser(PublicUser):
    cpf: str

