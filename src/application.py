import logging

import starlette.status

import models
from pydantic import BaseModel
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from user import get_current_user

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
    applications = db.query(models.UserApplication).filter(models.UserApplication.house_id == house).all()
    usernames = []
    for app in applications:
        user = db.query(models.User).filter(models.User.user_id == app.user_id).first()
        usernames.append((user.username, app.user_application_id))
    return templates.TemplateResponse("applications.html", {"request": request, "applications": usernames,
                                                            "user_id": user_id})


@router.post('/application/reject')
async def reject_application(application: ApplicationBase):
    print(application.application_id)


@router.post('/application/accept')
async def accept_application(application: ApplicationBase, db: Session = Depends(get_db)):
    app = db.query(models.UserApplication).filter(
        models.UserApplication.user_application_id == application.application_id).first()
    if not app:
        # if raises, we'd fuck'd up
        print('application not found')
        raise HTTPException(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR)
    print(app.house_id, app.user_application_id, app.user_id)
    house = db.query(models.House).filter(models.House.house_id == app.house_id).first()
    if not house:
        # if raises, we also have fuck'd up
        print('house not found')
        raise HTTPException(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR)
    # perform server side instead of here
    house.available = False
    db.flush()
    db.commit()
    print(house.available)
