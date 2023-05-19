import models
from sqlalchemy.orm import Session

from user import get_current_user
from fastapi import APIRouter, Request, Depends
from db import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="./templates")

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/home')
async def home(request: Request, response_class=HTMLResponse, user_id: str = Depends(get_current_user),
               db: Session = Depends(get_db)):
    houses = db.query(models.House).filter(models.House.available==True).all()
    houses = list(map(lambda h: (h.house_id, h.description, h.start_date, h.end_date, h.owner_id), houses))
    return templates.TemplateResponse("home.html", {"request": request, "houses": houses, "user_id": user_id})


@router.get('/add_my_home')
async def add_my_home(request: Request):
    try:
        redirect_url = request.url_for('my_home')
        return RedirectResponse(redirect_url)
    except Exception as _e:
        print(_e)


@router.get('/my_home')
async def my_home(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("my_home.html", {"request": request})
