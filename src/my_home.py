import models
from fastapi import APIRouter, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import get_db
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from user import get_current_user

templates = Jinja2Templates(directory="./templates")

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/create_home')
async def create_home(request: Request,
                      description: str = Form(...),
                      start_date: str = Form(...),
                      end_date: str = Form(...),
                      db: Session = Depends(get_db)):
    try:
        db.add(models.House(description=description, start_date=start_date, end_date=end_date,
                            owner_id=get_current_user()))
        db.commit()
        redirect_url = request.url_for('home')
        return RedirectResponse(redirect_url, status_code=HTTP_302_FOUND)
    except Exception as _e:
        print(_e)
