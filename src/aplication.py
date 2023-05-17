from fastapi import APIRouter, Form, Request, HTTPException
from typing_extensions import Annotated
from db import aplicate_to_house, view_aplications
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="./src/templates")

router = APIRouter()

@router.get('/aplication')
async def aplication(request: Request, response_class=HTMLResponse, username: str = None, house: str = None):
    aplicate_to_house(username, house)

@router.get('/aplications/{username}/{house}')
async def aplications(request: Request, response_class=HTMLResponse, username: str = None, house: str = None):
    return templates.TemplateResponse("aplications.html", {"request": request, "aplications": view_aplications(house), "username": username})
