from fastapi import APIRouter, status
from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from pydantic import BaseModel
from database.connection import *
from typing import Union
from datetime import datetime

users = APIRouter(
    prefix="/user", tags=["user"]
)

template = Jinja2Templates(directory='resources/views')


async def isUsers(request: Request) -> dict:
    id = request.cookies.get('id')

    if not id:
        return RedirectResponse('/login')

    res = await getUser(int(id))

    if res.get('role') == "Администратор":
        return {
            "admin": True,
            "materOt": False,
            "user": False
        }
    elif res.get('role') == "Материально. отвественный":
        return {
            "admin": False,
            "materOt": True,
            "user": False
        }
    elif res.get('role') == "Преподаватель":
        return {
            "admin": False,
            "materOt": False,
            'user': True
        }


@users.get('/')
async def index(request: Request):

    auth = request.cookies.get('Auth')

    if not auth:
        return RedirectResponse('/login')

    rs = await isUsers(request)

    if not rs.get('user'):
        return RedirectResponse('/login')

    return template.TemplateResponse('user/index.j2', {'request': request})
