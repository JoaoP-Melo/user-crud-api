from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    idade: Mapped[int] = mapped_column(Integer)
    estado: Mapped[str] = mapped_column(String(2))
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)