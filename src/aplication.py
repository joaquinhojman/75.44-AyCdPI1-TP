import models
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from db import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from user import get_current_user

templates = Jinja2Templates(directory="./templates")

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/aplication')
async def aplication(request: Request, response_class=HTMLResponse, user_id: str = Depends(get_current_user),
                     house_id: str = None, db: Session = Depends(get_db)):
    db.add(models.UserApplication(user_id=user_id, house_id=house_id))
    db.commit()


@router.get('/aplications/{house}')
async def aplications(request: Request, response_class=HTMLResponse, user_id: str = Depends(get_current_user),
                      house_id: str = None, db: Session = Depends(get_db)):
    applications = db.query(models.UserApplication).filter(models.UserApplication.house_id == house_id).all()
    usernames = []
    for app in applications:
        user = db.query(models.User).filter(models.User.user_id == app.user_id).first()
        usernames.append(user.username)
    return templates.TemplateResponse("aplications.html", {"request": request, "aplications": usernames,
                                                           "user_id": user_id})
