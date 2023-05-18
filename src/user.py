from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

CURRENT_USER = None

def get_current_user():
    global CURRENT_USER
    if CURRENT_USER is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    return CURRENT_USER

def set_current_user(user_id):
    global CURRENT_USER
    CURRENT_USER = user_id