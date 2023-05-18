from fastapi import APIRouter, Form, Request, HTTPException, Depends
from typing_extensions import Annotated
from db import aplicate_to_house, view_aplications
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from user import get_current_user

templates = Jinja2Templates(directory="./src/templates")

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post('/aplication')
async def aplication(request: Request, response_class=HTMLResponse, username: str = Depends(get_current_user), house: str = None):
    aplicate_to_house(username, house)

@router.get('/aplications/{house}')
async def aplications(request: Request, response_class=HTMLResponse, username: str = None, house: str = None):
    return templates.TemplateResponse("aplications.html", {"request": request, "aplications": view_aplications(house), "username": username})
