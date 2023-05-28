from operator import or_
import models
from sqlalchemy.orm import Session

from user import get_current_user
from fastapi import APIRouter, Form, Request, Depends
from db import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from functools import reduce

templates = Jinja2Templates(directory="./templates")

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/home')
async def home(request: Request, response_class=HTMLResponse, user_id: str = Depends(get_current_user),
               db: Session = Depends(get_db)):
    return templates.TemplateResponse("home2.html", {"request": request})#, "houses": new_houses, "user_id": user_id, "user": user})


@router.get('/add_my_home')
async def add_my_home(request: Request):
    try:
        redirect_url = request.url_for('my_home')
        return RedirectResponse(redirect_url)
    except Exception as _e:
        print(_e)


@router.get('/my_home')
async def my_home(request: Request, response_class=HTMLResponse, db: Session = Depends(get_db)):
    animals = db.query(models.Animal).all()
    animals = list(map(lambda a: a.animal_id, animals))
    return templates.TemplateResponse("my_home.html", {"request": request, "animals": animals})

@router.post("/edit", response_class=HTMLResponse)
def edit(request: Request, age: str = Form(...), country: str = Form(...), description: str = Form(...), db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    user = db.query(models.User)\
        .filter(models.User.user_id == user_id)\
        .first()
    user.age = age
    user.country = country
    user.description = description
    db.commit()
    return templates.TemplateResponse("home2.html", {"request": request, "user_id": user_id, "user": user})

@router.get("/profile")
def profile(request: Request, response_class=HTMLResponse, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    user = db.query(models.User)\
        .filter(models.User.user_id == user_id)\
        .first()
    return templates.TemplateResponse("profile.html", {"request": request, "user_id": user_id, "user": user})

@router.get("/view_my_homes")
def view_my_homes(request: Request, response_class=HTMLResponse, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    houses = db.query(models.House).filter(or_(
            models.House.available==True, models.House.owner_id == user_id
        )).all()
    houses = list(map(lambda h: (h.house_id, h.description, h.start_date, h.end_date, h.owner_id, h.city, h.rooms, h.available), houses))

    new_houses = []
    for house in houses:
        pets = db.query(models.Pet).filter(models.Pet.house_id == house[0]).all()
        pets_list = list(map(lambda p: (p.animal_id, p.pet_cant), pets))
        new_houses.append((*house, [*pets_list]))
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return templates.TemplateResponse("my_homes.html", {"request": request, "houses": new_houses, "user_id": user_id, "user": user})

@router.get("/search_homes")
def search_homes(request: Request, response_class=HTMLResponse, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    houses = db.query(models.House).filter(or_(
            models.House.available==True, models.House.owner_id == user_id
        )).all()
    houses = list(map(lambda h: (h.house_id, h.description, h.start_date, h.end_date, h.owner_id, h.city, h.rooms, h.available), houses))

    new_houses = []
    for house in houses:
        pets = db.query(models.Pet).filter(models.Pet.house_id == house[0]).all()
        pets_list = list(map(lambda p: (p.animal_id, p.pet_cant), pets))
        new_houses.append((*house, [*pets_list]))
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return templates.TemplateResponse("search_homes.html", {"request": request, "houses": new_houses, "user_id": user_id, "user": user})

@router.get('/house_details/{house_id}')
async def house_details(request: Request, response_class=HTMLResponse, house_id: int=None, db: Session = Depends(get_db)):
    house = db.query(models.House).filter(models.House.house_id == house_id).first()
    pets = db.query(models.Pet).filter(models.Pet.house_id == house_id).all()
    pets_list = list(map(lambda p: (p.animal_id, p.pet_cant), pets))

    return templates.TemplateResponse("house_details.html", {"request": request, "house": house, "pets": pets_list})
