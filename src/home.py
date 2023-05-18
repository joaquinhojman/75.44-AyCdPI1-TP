from user import get_current_user
from fastapi import APIRouter, Form, Request, HTTPException, Depends
from typing_extensions import Annotated
from db import read_houses
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="./src/templates")

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get('/home')
async def home(request: Request, response_class=HTMLResponse, username: str = Depends(get_current_user)):
    return templates.TemplateResponse("home.html", {"request": request, "houses": read_houses(), "username": username})

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
