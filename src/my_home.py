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
                      city: str = Form(...),
                      room: str = Form(...),
                      Perro_cant: str = Form(...),
                      Gato_cant: str = Form(...),
                      Ave_cant: str = Form(...),
                      Pez_cant: str = Form(...),
                      Araña_cant: str = Form(...),
                      Serpiente_cant: str = Form(...),
                      Huron_cant: str = Form(...),
                      Erizo_cant: str = Form(...),
                      Morsa_cant: str = Form(...),
                      Carpincho_cant: str = Form(...),
                      Otro_cant: str = Form(...),
                      db: Session = Depends(get_db)):
    pets = {}
    pets['Perro'] = Perro_cant
    pets['Gato'] = Gato_cant
    pets['Ave'] = Ave_cant
    pets['Pez'] = Pez_cant
    pets['Araña'] = Araña_cant
    pets['Serpiente'] = Serpiente_cant
    pets['Huron'] = Huron_cant
    pets['Erizo'] = Erizo_cant
    pets['Morsa'] = Morsa_cant
    pets['Carpincho'] = Carpincho_cant
    pets['Otro'] = Otro_cant
    
    try:
        house = models.House(description=description, start_date=start_date, end_date=end_date,
                                    city=city, rooms=room,
                            owner_id=get_current_user())
        db.add(house)
        db.commit()

        house_id = house.house_id
        for k,v in pets.items():
            if int(v) == 0: continue
            db.add(models.Pet(house_id=house_id, animal_id=k, pet_cant=int(v)))
        db.commit()
        redirect_url = request.url_for('home')
        return RedirectResponse(redirect_url, status_code=HTTP_302_FOUND)
    except Exception as _e:
        print(_e)
