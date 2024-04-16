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


@users.get('/property')
async def property(request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return RedirectResponse('/login')
    rs = await isUsers(request)
    if not rs.get('user'):
        return RedirectResponse('/login')

    emu = await selectPropetry()

    if not emu:
        emu = []

    new_emu = []

    for i in emu:
        id, name, datestart, cost, costyear, costafter, period, hallid = i
        new_emu.append({
            'id': id,
            'name': name,
            'datestart': datestart,
            'cost': cost,
            'costyear': costyear,
            'costafter': costafter,
            'period': period,
            'hallid': hallid
        })

    return template.TemplateResponse('user/equipment.j2', {'request': request, "emu": new_emu})


@users.get('/building')
async def building(request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return RedirectResponse('/login')
    rs = await isUsers(request)
    if not rs.get('user'):
        return RedirectResponse('/login')

    emu = await selectBuilding()

    if not emu:
        emu = []

    new_emu = []

    for i in emu:
        id, id_kadastr, buildingname, land, material, wear, flow, comment = i

        kadastr = await getBuildingKadastr(id_kadastr)

        id_kad, street, house, year = kadastr

        new_emu.append({
            'id': id,
            'kadastr': {
                "street": street,
                "house": house,
                "year": year
            },
            'buildingname': buildingname,
            'land': land,
            'material': material,
            'wear': wear,
            'flow': flow,
            'comment': comment
        })

    return template.TemplateResponse('user/building.j2', {'request': request, "emu": new_emu})


@users.get('/kadastr')
async def kadastr(request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return RedirectResponse('/login')
    rs = await isUsers(request)
    if not rs.get('user'):
        return RedirectResponse('/login')

    emu = await selectKadastr()
    if not emu:
        emu = []

    new_emu = []

    for i in emu:
        id, street, house, year = i
        new_emu.append({
            'id': id,
            'street': street,
            'house': house,
            'year': year
        })

    return template.TemplateResponse('user/kadastr.j2', {'request': request, "emu": new_emu})
