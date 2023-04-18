from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Reciclado(SQLModel, table=True):
    id:int= Field(primary_key=True)
    tipo: str
    peso: float

class Depto(SQLModel, table=True):
    id: int= Field(primary_key=True)
    name: str
    direccion: str

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    name: str
    password: str
    depto:int = Field(foreign_key="depto.id")
    numero_depto: int
    cantidad_personas: int
    email: str = Field(default=None, nullable=True)

class SalaBasura(SQLModel, table=True):
    id:int = Field(primary_key=True)
    id_carousel: str
    url_carousel: str
    depto:int = Field(foreign_key="depto.id")

class Instancias(SQLModel, table=True):
    depto:int = Field(foreign_key="depto.id",primary_key=True)
    depto:int = Field(foreign_key="reciclado.id",primary_key=True)
    date: datetime = Field(default_factory=datetime.utcnow)