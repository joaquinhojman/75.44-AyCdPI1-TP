from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.db import user_create, user_exists

templates = Jinja2Templates(directory="./src/templates")

router = APIRouter()

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    exists, _ = user_exists(username=username)
    if not exists:
        user_create(username=username, password=password)
        return templates.TemplateResponse("login.html", {"request": request, "username": username})
    raise HTTPException(status_code=401, detail="User already exists")