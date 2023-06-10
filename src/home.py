from operator import or_, and_
import models
from sqlalchemy.orm import Session

from user import get_current_user
from fastapi import APIRouter, Form, Request, Depends
from db import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from functools import reduce

from datetime import datetime

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

def formatFecha(fecha):
    fecha = datetime.strptime(str(fecha), "%Y-%m-%d %H:%M:%S")
    formato = fecha.strftime("%A, %B %d %Y")
    return formato

@router.get("/view_my_homes")
def view_my_homes(request: Request, response_class=HTMLResponse, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    houses = db.query(models.House).filter(or_(
            models.House.available==True, models.House.owner_id == user_id
        )).all()
    houses = list(map(lambda h: (h.house_id, h.description, formatFecha(h.start_date), formatFecha(h.end_date), h.owner_id, h.city, h.rooms, h.available), houses))

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
    houses = list(map(lambda h: (h.house_id, h.description, formatFecha(h.start_date), formatFecha(h.end_date), h.owner_id, h.city, h.rooms, h.available), houses))

    new_houses = []
    for house in houses:
        pets = db.query(models.Pet).filter(models.Pet.house_id == house[0]).all()
        pets_list = list(map(lambda p: (p.animal_id, p.pet_cant), pets))

        owner_id = house[4]
        owner_houses = db.query(models.House).filter(models.House.owner_id == str(owner_id)).all()
        owner_houses = list(map(lambda h: h.house_id, owner_houses))
        ratings = []
        comments = []
        for owner_house in owner_houses:
            rating = db.query(models.RatingsHouses).filter(models.RatingsHouses.house_id == str(owner_house)).all()
            house_comments = list(map(lambda u: u.comment, rating))
            house_ratings = list(map(lambda u: u.rating, rating))
            ratings.extend(house_ratings)
            comments.extend(house_comments)

        mean_user_rating = 0 if not ratings else sum(ratings) / len(ratings)
        comments = comments[:min(len(comments), 5)]
        new_houses.append((*house, [*pets_list], mean_user_rating, [*comments]))
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return templates.TemplateResponse("search_homes.html", {"request": request, "houses": new_houses, "user_id": user_id, "user": user})

@router.get('/house_details/{house_id}')
async def house_details(request: Request, response_class=HTMLResponse, house_id: int=None, db: Session = Depends(get_db)):
    house = db.query(models.House).filter(models.House.house_id == house_id).first()
    pets = db.query(models.Pet).filter(models.Pet.house_id == house_id).all()
    pets_list = list(map(lambda p: (p.animal_id, p.pet_cant), pets))
    house.start_date = formatFecha(house.start_date)
    house.end_date = formatFecha(house.end_date)

    return templates.TemplateResponse("house_details.html", {"request": request, "house": house, "pets": pets_list})

@router.get('/view_my_applications')
async def view_my_applications(request: Request, response_class=HTMLResponse, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    applications = db.query(models.UserApplication).filter(models.UserApplication.user_id == user_id).all()
    applications = list(map(lambda h: (h.user_application_id, h.user_id, h.house_id, h.accepted), applications))

    new_applications = []
    for application in applications:
        house = db.query(models.House).filter(models.House.house_id == application[2]).first()
        rating = db.query(models.RatingsHouses).filter(and_(models.RatingsHouses.house_id == str(house.house_id), models.RatingsHouses.user_id == str(user_id))).first()
        new_applications.append((application[3], house.description, formatFecha(house.start_date), formatFecha(house.end_date), house.city, house.house_id, rating.rating if rating != None else None, rating.comment if rating != None else None))

    print(new_applications)
    return templates.TemplateResponse("view_my_applications.html", {"request": request, "applications": new_applications})


@router.post('/search_with_filter')
async def search_with_filter(request: Request,
                    start_date: str = Form(None),
                    end_date: str = Form(None),
                    city: str = Form(None),
                    pet: str = Form(None),
                    db: Session = Depends(get_db),
                    user_id: str = Depends(get_current_user)):
    query = db.query(models.House).filter(models.House.available==True)
        
    if start_date is not None:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(models.House.start_date >= start_datetime)

    if end_date is not None:
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.filter(models.House.end_date <= end_datetime)

    if city is not None:
        query = query.filter(models.House.city.ilike(f"%{city}%"))
    
    if pet is not None:
        query = query.join(models.Pet, models.House.house_id == models.Pet.house_id).filter(models.Pet.animal_id == pet)
    
    result = query.all()
    
    houses = list(map(lambda h: (h.house_id, h.description, formatFecha(h.start_date), formatFecha(h.end_date), h.owner_id, h.city, h.rooms, h.available), result))
    print(houses)

    new_houses = []
    for house in houses:
        pets = db.query(models.Pet).filter(models.Pet.house_id == house[0]).all()
        pets_list = list(map(lambda p: (p.animal_id, p.pet_cant), pets))

        owner_id = house[4]
        owner_houses = db.query(models.House).filter(models.House.owner_id == str(owner_id)).all()
        owner_houses = list(map(lambda h: h.house_id, owner_houses))
        ratings = []
        comments = []
        for owner_house in owner_houses:
            rating = db.query(models.RatingsHouses).filter(models.RatingsHouses.house_id == str(owner_house)).all()
            house_comments = list(map(lambda u: u.comment, rating))
            house_ratings = list(map(lambda u: u.rating, rating))
            ratings.extend(house_ratings)
            comments.extend(house_comments)

        mean_user_rating = 0 if not ratings else sum(ratings) / len(ratings)
        comments = comments[:min(len(comments), 5)]
        new_houses.append((*house, [*pets_list], mean_user_rating, [*comments]))
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return templates.TemplateResponse("search_with_filter.html", {"request": request, "houses": new_houses, "user_id": user_id, "user": user})
