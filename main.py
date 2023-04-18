from fastapi import FastAPI
import uvicorn
from sqlmodel import create_engine, SQLModel, Session, select
from models.models import *

app = FastAPI()

engine = create_engine("sqlite:///database.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    populate_db()

def populate_db():
    depto1 = Depto(name="depto1",direccion="Calle falsa 123")
    user1 = User(username="Username1",name="Name",password="Password",depto=1,numero_depto=123,cantidad_personas=2)
    with Session(engine) as session:
        session.add(depto1)
        session.add(user1)
        session.commit()

@app.get("/")
def index():
    with Session(engine) as session:
        stmt = select(User)
        users = session.exec(stmt).all()
    return users

if __name__ == '__main__':
    create_db_and_tables()
    uvicorn.run(app, host="localhost", port=8080)
    