import uvicorn
import login as login
import models
import register as register
import home as home
import my_home as my_home
import application as application
from db import engine, Base, get_db
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Animal

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(login.router)
app.include_router(register.router)
app.include_router(home.router)
app.include_router(my_home.router)
app.include_router(application.router)

app.mount('/static', StaticFiles(directory='./static'), name='static')

try:
    db = next(get_db())
    animals = []
    animals.append(Animal(animal_id='Perro'))
    animals.append(Animal(animal_id='Gato'))
    animals.append(Animal(animal_id='Ave'))
    animals.append(Animal(animal_id='Pez'))
    #animals.append(Animal(animal_id='Araña'))
    #animals.append(Animal(animal_id='Serpiente'))
    #animals.append(Animal(animal_id='Huron'))
    #animals.append(Animal(animal_id='Erizo'))
    #animals.append(Animal(animal_id='Morsa'))
    #animals.append(Animal(animal_id='Carpincho'))
    animals.append(Animal(animal_id='Otro'))
    db.add_all(animals)
    db.commit()
except Exception as _e:
    pass

templates = Jinja2Templates(directory="./templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, log_level="info")
