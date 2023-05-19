from fastapi import APIRouter, Form, Request, HTTPException, Depends
from typing_extensions import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import models
from db import get_db
from fastapi.responses import RedirectResponse
from starlette import status
from user import set_current_user
from sqlalchemy.orm import Session

templates = Jinja2Templates(directory="./templates")

router = APIRouter()


@router.post('/login')
async def login(request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()],
                response_class=HTMLResponse, db: Session = Depends(get_db)):
    user = (
        db
        .query(models.User)
        .filter(models.User.username == username)
        .filter(models.User.password == password).first()
    )
    if user and user.username == username and user.password == password:
        set_current_user(user.user_id)
        redirect_url = request.url_for('home')
        return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
    raise HTTPException(status_code=401, detail='User or password invalid')


@router.get('/login')
async def login(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get('/logout')
def logout():
    raise NotImplementedError()
