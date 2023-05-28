import logging
from operator import and_

import starlette.status

import models
from pydantic import BaseModel
from fastapi import APIRouter, Form, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from user import get_current_user
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="./templates")

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


class ApplicationBase(BaseModel):
    application_id: int


class HouseBase(BaseModel):
    house_id: int


@router.post('/application')
async def application(response_class=HTMLResponse, user_id: str = Depends(get_current_user),
                      house: HouseBase = None, db: Session = Depends(get_db)):
    db.add(models.UserApplication(user_id=user_id, house_id=house.house_id))
    db.commit()


@router.get('/applications/{house}')
async def applications(request: Request, response_class=HTMLResponse, user_id: str = Depends(get_current_user),
                       house: int = None, db: Session = Depends(get_db)):
    applications = db.query(models.UserApplication).filter(and_(
        models.UserApplication.house_id == house,
        models.UserApplication.accepted == None
    )).all()
    usernames = []
    for app in applications:
        user = db.query(models.User).filter(models.User.user_id == app.user_id).first()
        user_ratings = db.query(models.Ratings).filter(models.Ratings.user_id == str(app.user_id)).all()
        mean_user_rating = 0 if not user_ratings else sum((rating for rating in list(map(lambda u: u.rating, user_ratings)))) / len(user_ratings)
        comments = list(map(lambda u: u.comment, user_ratings))
        print(comments)
        comments = comments[:min(len(comments), 5)]
        print(comments)
        usernames.append((user.username, app.user_application_id, user.description, user.country, user.age, mean_user_rating, comments))
    
    return templates.TemplateResponse("applications.html", {"request": request, "applications": usernames,
                                                            "user_id": user_id})

@router.get('/applications_confirmed/{house}')
async def applications_confirmed(request: Request, response_class=HTMLResponse, user_id: str = Depends(get_current_user),
                       house: int = None, db: Session = Depends(get_db)):
    application = db.query(models.UserApplication).filter(and_(
        models.UserApplication.house_id == house,
        models.UserApplication.accepted == True
    )).first()
    user = db.query(models.User).filter(models.User.user_id == application.user_id).first()
    rating = db.query(models.Ratings).filter(and_(models.Ratings.user_id == str(user.user_id), models.Ratings.house_id == str(house))).first()
    return templates.TemplateResponse("applications_confirmed.html", {"request": request, "user": user, "user_id": user_id, "house_id": house, "rating": rating})


@router.post('/application/reject')
async def reject_application(request: Request, application: ApplicationBase, db: Session = Depends(get_db)):
    app = db.query(models.UserApplication).filter(
        models.UserApplication.user_application_id == application.application_id).first()
    if not app:
        print('application not found')
        raise HTTPException(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR)
    app.accepted = False
    db.commit()

@router.post('/application/accept')
async def accept_application(application: ApplicationBase, db: Session = Depends(get_db)):
    app = db.query(models.UserApplication).filter(
        models.UserApplication.user_application_id == application.application_id).first()
    if not app:
        # if raises, we'd fuck'd up
        print('application not found')
        raise HTTPException(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR)
    house = db.query(models.House).filter(models.House.house_id == app.house_id).first()
    if not house:
        # if raises, we also have fuck'd up
        print('house not found')
        raise HTTPException(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR)
    # perform server side instead of here
    house.available = False
    app.accepted = True
    db.flush()
    db.commit()


@router.post('/rate_applicant/{user_id}/{house_id}')
async def rate_applicant(request: Request, user_id, house_id, db: Session = Depends(get_db), rating = Form(...), comment = Form(None)):
    row = db.query(models.Ratings).filter(models.Ratings.user_id == user_id).filter(models.Ratings.house_id == house_id).first()
    if row:
        row.rating = rating
        if comment:
            row.comment = comment
    else:
        db.add(models.Ratings(
            user_id=user_id,
            house_id=house_id,
            rating=rating,
            comment=comment))
    db.commit()

    redirect_url = request.url_for('applications_confirmed', house=house_id)
    return RedirectResponse(redirect_url, status_code=starlette.status.HTTP_302_FOUND)