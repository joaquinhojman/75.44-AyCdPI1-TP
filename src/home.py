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
    houses = db.query(models.House).filter(models.House.available==True).all()
    houses = list(map(lambda h: (h.house_id, h.description, h.start_date, h.end_date, h.owner_id, h.city, h.rooms), houses))

    new_houses = []
    for house in houses:
        pets = db.query(models.Pet).filter(models.Pet.house_id == house[0]).all()
        pets_list = list(map(lambda p: (p.animal_id, p.pet_cant), pets))
        new_houses.append((*house, [*pets_list]))
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return templates.TemplateResponse("home.html", {"request": request, "houses": new_houses, "user_id": user_id, "user": user})


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
    return templates.TemplateResponse("home.html", {"request": request, "user_id": user_id, "user": user})
