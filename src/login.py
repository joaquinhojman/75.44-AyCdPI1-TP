from fastapi import APIRouter, Form, Request, HTTPException
from typing_extensions import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import user_exists


templates = Jinja2Templates(directory="./src/templates")

router = APIRouter()

@router.post('/login')
def login(request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()], response_class=HTMLResponse):
    exists, user_pass = user_exists(username=username)
    if exists and user_pass[0] == username and user_pass[1] == password:
        return templates.TemplateResponse("home.html", {"request": request})
    raise HTTPException(status_code=401, detail='User or password invalid')


@router.get('/login')
async def login(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get('/logout')
def logout():
    raise NotImplementedError()