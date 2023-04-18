from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import IntEnum

class DesechoEnum(IntEnum):
    plastico =1
    vidrio =2
    lata =3
    basura =4


class Desecho(SQLModel, table=True):
    id:int= Field(primary_key=True)
    tipo: DesechoEnum = Field(default=DesechoEnum.basura)
    peso: float
    date: datetime = Field(default_factory=datetime.utcnow)
    id_user:int = Field(foreign_key="user.id")

class Depto(SQLModel, table=True):
    id: int= Field(primary_key=True)
    name: str
    direccion: str

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    name: str
    password: str
    id_depto:int = Field(foreign_key="depto.id")
    numero_depto: int
    cantidad_personas: int
    email: str = Field(default=None, nullable=True)

class SalaBasura(SQLModel, table=True):
    id:int = Field(primary_key=True)
    id_carousel: str
    url_carousel: str
    id_depto:int = Field(foreign_key="depto.id")
