import os
from fastapi import FastAPI, Request, Body
from fastapi.responses import RedirectResponse
import uvicorn
from datetime import datetime
from sqlmodel import create_engine, SQLModel, Session, select, func
from fastapi.middleware.cors import CORSMiddleware
from models.models import *
from auth.auth import *


app = FastAPI()
auth_handler= AuthHandler()

engine = create_engine("sqlite:///database.db")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        desecho2 = Desecho(tipo=DesechoEnum.lata,peso=2, id_user=user2.id)
        desecho3 = Desecho(tipo=DesechoEnum.basura,peso=3, id_user=user2.id)
        desecho4 = Desecho(tipo=DesechoEnum.lata,peso=1.2, id_user=user3.id)
        desecho5 = Desecho(tipo=DesechoEnum.lata,peso=1.1, id_user=user4.id)
        desecho6 = Desecho(tipo=DesechoEnum.plastico,peso=0.76, id_user=user5.id)
        desecho7 = Desecho(tipo=DesechoEnum.basura,peso=1.5, id_user=user5.id)
        desecho8 = Desecho(tipo=DesechoEnum.plastico,peso=6, id_user=user3.id)

        session.add(desecho1)
        session.add(desecho2)
        session.add(desecho3)
        session.add(desecho4)
        session.add(desecho5)
        session.add(desecho6)
        session.add(desecho7)
        session.add(desecho8)

        session.commit()


@app.post("/login")
async def login(request: Request, item: dict = Body(...)):
    with Session(engine) as session:

        sqlResponse= session.query(User).filter(User.username == item["username"]).first()

        if sqlResponse!=None:
            if auth_handler.verify_password(item["password"],sqlResponse.password):
                raise HTTPException(status_code=200, detail= str(sqlResponse.id))
            
        raise HTTPException(status_code=401, detail="Bad Credentials")

@app.post("/dispose")
async def dispose(request: Request, item: dict = Body(...)):


    with Session(engine) as session:

        sqlResponse= session.query(User).filter(User.username == item["username"]).first()
        userID=sqlResponse.id
        
        newDesecho= Desecho(tipo=DesechoEnum(item["desecho"]),peso=item["peso"], id_user=userID)
        session.add(newDesecho)
        session.commit()

        raise HTTPException(status_code=200, detail="Waste Disposed")

@app.post("/userinfo")
async def userinfo(request: Request, item: dict = Body(...)):
    with Session(engine) as session:

        stmt = select(User.username, User.name, Depto.name).join(Depto, User.id_depto == Depto.id).where(User.id == item["user_id"])

        # Execute the query and fetch the results
        results = session.exec(stmt).all()

        return {
            "username":results[0]["username"],
            "name":results[0]["name"],
            "depto_name":results[0]["name_1"]
        }

@app.post("/userwasteinfo")
async def userwasteinfo(request: Request, item: dict = Body(...)):
    chartData=[]

    totalSumPlas=0
    totalSumVidr=0
    totalSumLat=0

    totalSumPlasMONTH=0
    totalSumVidrMONTH=0
    totalSumLatMONTH=0
    
    with Session(engine) as session:

        stmt = select(User.name, Depto.name,Desecho.tipo, Desecho.peso, Desecho.date).join(Depto, User.id_depto == Depto.id).join(Desecho, User.id == Desecho.id_user).where(User.id == item["user_id"])
        stmt2 = select(func.extract('year', Desecho.date).label('year'),func.extract('month', Desecho.date).label('month'),func.sum(Desecho.peso)).select_from(User.__table__.join(Desecho, User.id == Desecho.id_user)).where(User.id == item["user_id"]).where(Desecho.tipo!=4).group_by(func.extract('year', Desecho.date),func.extract('month', Desecho.date))
        # Execute the query and fetch the results
        results = session.exec(stmt).all()
        results2 = session.exec(stmt2).all()

        for data in results:
            if(data["date"].month ==datetime.datetime.now().month):

                if (data["tipo"]==1):
                    totalSumPlasMONTH+=data["peso"]
                if (data["tipo"]==2):
                    totalSumVidrMONTH+=data["peso"]
                if (data["tipo"]==3):
                    totalSumLatMONTH+=data["peso"]

            if (data["tipo"]==1):
                totalSumPlas+=data["peso"]
            if (data["tipo"]==2):
                totalSumVidr+=data["peso"]
            if (data["tipo"]==3):
                totalSumLat+=data["peso"]
        
        for data in results2:
            chartData.append(data)
        
        return {
            "username":results[0]["name"],
            "depto_name":results[0]["name_1"],
            "totalSumPlas":totalSumPlas,
            "totalSumVidr":totalSumVidr,
            "totalSumLat":totalSumLat,
            "totalSumPlasMONTH":totalSumPlasMONTH,
            "totalSumVidrMONTH":totalSumVidrMONTH,
            "totalSumLaMONTH":totalSumLatMONTH,
            "chartData":chartData
        }

@app.post("/deptowasteinfo")
async def deptowasteinfo(request: Request, item: dict = Body(...)):
    chartData=[]
    leaderBoard=[]

    totalSumPlas=0
    totalSumVidr=0
    totalSumLat=0

    totalSumPlasMONTH=0
    totalSumVidrMONTH=0
    totalSumLatMONTH=0

    totalSumPlasYEAR=0
    totalSumVidrYEAR=0
    totalSumLatYEAR=0
    
    with Session(engine) as session:

        id_depto= session.query(User).filter(User.id == item["user_id"]).first().id_depto
        stmt = select(Depto.name,Depto.direccion, Desecho.tipo, Desecho.peso, Desecho.date).join(User, User.id_depto == Depto.id).join(Desecho, User.id == Desecho.id_user).where(Depto.id == id_depto)
        stmt2 = select(func.extract('year', Desecho.date).label('year'),func.extract('month', Desecho.date).label('month'),func.sum(Desecho.peso)).select_from(Depto.__table__.join(User, User.id_depto == Depto.id).join(Desecho, User.id == Desecho.id_user)).where(Depto.id == id_depto).where(Desecho.tipo!=4).group_by(func.extract('year', Desecho.date),func.extract('month', Desecho.date))
        stmt3 = select(User.numero_depto,func.sum(Desecho.peso)).join(Depto, User.id_depto == Depto.id).join(Desecho, User.id == Desecho.id_user).where(Depto.id == id_depto).group_by(User.numero_depto).order_by(func.sum(Desecho.peso).desc()).limit(5)
        
        results = session.exec(stmt).all()
        results2 = session.exec(stmt2).all()
        results3 = session.exec(stmt3).all()

        for data in results:
            if(data["date"].month ==datetime.datetime.now().month):

                if (data["tipo"]==1):
                    totalSumPlasMONTH+=data["peso"]
                if (data["tipo"]==2):
                    totalSumVidrMONTH+=data["peso"]
                if (data["tipo"]==3):
                    totalSumLatMONTH+=data["peso"]

            if(data["date"].year ==datetime.datetime.now().year):

                if (data["tipo"]==1):
                    totalSumPlasYEAR+=data["peso"]
                if (data["tipo"]==2):
                    totalSumVidrYEAR+=data["peso"]
                if (data["tipo"]==3):
                    totalSumLatYEAR+=data["peso"]

            if (data["tipo"]==1):
                totalSumPlas+=data["peso"]
            if (data["tipo"]==2):
                totalSumVidr+=data["peso"]
            if (data["tipo"]==3):
                totalSumLat+=data["peso"]
        
        for data in results2:
            chartData.append(data)
        
        for data in results3:
            leaderBoard.append(data)

        return {
            "name":results[0]["name"],
            "address":results[0]["direccion"],
            "totalSumPlas":totalSumPlas,
            "totalSumVidr":totalSumVidr,
            "totalSumLat":totalSumLat,
            "totalSumPlasMONTH":totalSumPlasMONTH,
            "totalSumVidrMONTH":totalSumVidrMONTH,
            "totalSumLaMONTH":totalSumLatMONTH,
            "totalSumPlasYEAR":totalSumPlasYEAR,
            "totalSumVidrYEAR":totalSumVidrYEAR,
            "totalSumLaYEAR":totalSumLatYEAR,
            "chartData":chartData,
            "leaderboard":leaderBoard
        }

if __name__ == '__main__':
    create_db_tables_populate()
    uvicorn.run(app, host="localhost", port=8080)
    