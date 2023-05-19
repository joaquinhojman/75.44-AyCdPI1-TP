import models
from fastapi import APIRouter, Form, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import get_db

templates = Jinja2Templates(directory="./templates")

router = APIRouter()


@router.get("/register", response_class=HTMLResponse)
def register(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
def register(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    exists = db.query(models.User)\
        .filter(models.User.username == email)\
        .filter(models.User.password == password)\
        .first()
    if not exists:
        db.add(models.User(username=email, password=password))
        db.commit()
        return templates.TemplateResponse("login.html", {"request": request, "email": email})
    raise HTTPException(status_code=401, detail="User already exists")
