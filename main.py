import os
from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
import uvicorn
from sqlmodel import create_engine, SQLModel, Session, select
from models.models import *
from auth.auth import *

app = FastAPI()
auth_handler= AuthHandler()

engine = create_engine("sqlite:///database.db")

def create_db_tables_populate():
    if os.path.exists("database.db"):
        os.remove("database.db")
    SQLModel.metadata.create_all(engine)
    populate_db()

def populate_db():
    with Session(engine) as session:       
        #Deptos
        depto1 = Depto(id=1,name="Departamento las Rosas",direccion="Calle Falsa 123")
        depto2 = Depto(id=2,name="Departamento los Olivos",direccion="Avenida Falsa 333")

        session.add(depto1)
        session.add(depto2)

        #Users
        password = auth_handler.get_password_hash("123")

        user1 = User(id=1,username="ed34Anon",name="Anon",password=password,id_depto=depto1.id,numero_depto=0,cantidad_personas=1, anon=True)

        user2 = User(id=2,username="ed34depto32",name="Joaquin",password=password,id_depto=depto1.id,numero_depto=32,cantidad_personas=2)
        user3 = User(id=3,username="ed34depto55",name="Matias",password=password,id_depto=depto1.id,numero_depto=55,cantidad_personas=4)

        user4 = User(id=4,username="ed11Anon",name="Anon",password=password,id_depto=depto2.id,numero_depto=0,cantidad_personas=1, anon=True)

        user5 = User(id=5,username="ed11depto12",name="Nicolas",password=password,id_depto=depto2.id,numero_depto=12,cantidad_personas=1)

        session.add(user1)
        session.add(user2)
        session.add(user3)
        session.add(user4)
        session.add(user5)

        #Sala Basura
        salaBasura1 = SalaBasura(id_carousel=1, url_carousel="URL", id_depto=depto1.id)
        salaBasura2 = SalaBasura(id_carousel=1, url_carousel="URL", id_depto=depto2.id)

        session.add(salaBasura1)
        session.add(salaBasura2)

        #Desechos
        desecho1 = Desecho(tipo=DesechoEnum.vidrio,peso=2.3, id_user=user1.id)
        desecho2 = Desecho(tipo=DesechoEnum.lata,peso=2, id_user=user1.id)
        desecho3 = Desecho(tipo=DesechoEnum.basura,peso=3, id_user=user1.id)
        desecho4 = Desecho(tipo=DesechoEnum.lata,peso=1.2, id_user=user1.id)
        desecho5 = Desecho(tipo=DesechoEnum.lata,peso=1.1, id_user=user1.id)
        desecho6 = Desecho(tipo=DesechoEnum.plastico,peso=0.76, id_user=user1.id)
        desecho7 = Desecho(tipo=DesechoEnum.basura,peso=1.5, id_user=user1.id)
        desecho8 = Desecho(tipo=DesechoEnum.plastico,peso=6, id_user=user1.id)

        session.add(desecho1)
        session.add(desecho2)
        session.add(desecho3)
        session.add(desecho4)
        session.add(desecho5)
        session.add(desecho6)
        session.add(desecho7)
        session.add(desecho8)

        session.commit()


@app.get("/")
def index():
    return RedirectResponse(url="/login")


@app.get("/login")
def loginGet():
    return "Login HTML"

@app.post("/login")
def loginPost(username: str = Form(...), password: str = Form(...)):
    
    with Session(engine) as session:

        sqlResponse= session.query(User).filter(User.username == username).first()

        if sqlResponse!=None:
            if auth_handler.verify_password(password,sqlResponse.password):
                return "Login Success"
            
        return "Login Failed"
            

if __name__ == '__main__':
    create_db_tables_populate()
    uvicorn.run(app, host="localhost", port=8080)
    