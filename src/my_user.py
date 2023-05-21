import models
from fastapi import APIRouter, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import get_db
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.status import HTTP_302_FOUND
from user import get_current_user

templates = Jinja2Templates(directory="./templates")

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/add_info')
async def add_user_info(request: Request,
                      name: str = Form(...),
                      last_name: str = Form(...),
                      pets: str = Form(...),
                      location: str = Form(...),
                      description: str = Form(...),
                      db: Session = Depends(get_db)):
    try:
        db.add(models.User(name=name, last_name=last_name, pets=pets, location=location, description=description))
        db.commit()
        redirect_url = request.url_for('my_user')
        return RedirectResponse(redirect_url, status_code=HTTP_302_FOUND)
    except Exception as _e:
        print(_e)


@router.get('/view_user/<id>')
async def view_user(id, request: Request, response_class=HTMLResponse, user_id: str = Depends(get_current_user),
               db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id==id).first()
    user_info = list(map(lambda u: (u.user_id, u.name, u.last_name, u.pets, u.location, u.description), user))
    return templates.TemplateResponse("my_user.html", {"request": request, "user_info": user_info, "user_id": id})
