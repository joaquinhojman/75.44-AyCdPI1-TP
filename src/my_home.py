from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import house_create
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="./src/templates")

router = APIRouter()


@router.post('/create_home')
def create_home(request: Request, description: str = Form(...), start_date: str = Form(...), end_date: str = Form(...)):
    try:
        house_create(description=description, start_date=start_date, end_date=end_date)
        redirect_url = request.url_for('home')    
        return RedirectResponse(redirect_url)
    except Exception as _e:
        print(_e)
