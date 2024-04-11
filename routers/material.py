from fastapi import APIRouter, status
from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from pydantic import BaseModel
from database.connection import *
from typing import Union
from datetime import datetime

template = Jinja2Templates(directory='resources/views')

materials = APIRouter(
    prefix='/materil',
    tags=['materials']
)


async def isUsers(request: Request) -> dict:
    id = request.cookies.get('id')

    res = await getUser(int(id))

    if not id:
        return RedirectResponse('/login')

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
    elif res.get('role') == "Пользователь":
        return {
            "admin": False,
            "materOt": False,
            'user': True
        }


@materials.get('/')
async def index(request: Request):

    auth = request.cookies.get('Auth')

    if not auth:
        return RedirectResponse('/login')

    user = await isUsers(request)

    if not user.get('materOt'):
        return RedirectResponse('/login')

    return template.TemplateResponse('financiallyResponsible/index.j2', {'request': request})


@materials.get('/property')
async def property(request: Request):
    auth = request.cookies.get('Auth')

    if not auth:
        return RedirectResponse('/login')

    user = await isUsers(request)

    if not user.get('materOt'):
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

    return template.TemplateResponse('financiallyResponsible/equipment.j2', {'request': request, 'emu': new_emu})


class EditProperty(BaseModel):
    unitid: int
    unitname: str
    datestart: datetime
    cost: float
    costyear: int
    costafter: int
    period: int
    hallid: int


class PropertyDelete(BaseModel):
    unitid: Union[str, int]


class PropertyCreate(BaseModel):
    unitname: str
    datestart: datetime
    cost: float
    costyear: int
    costafter: int
    period: int
    hallid: int


@materials.post('/property/create')
async def createProperty(property: PropertyCreate, request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return "redirect"
    user = await isUsers(request)
    if not user.get('materOt'):
        return "redirect"
    
    res = await createPropetry(property.unitname, property.datestart, property.cost, property.costyear, property.costafter, property.period, property.hallid)


@materials.get('/property/get/{item}')
async def getProperty(item: str, request: Request):
    auth = request.cookies.get('Auth')

    if not auth:
        return "redirect"

    user = await isUsers(request)

    if not user.get('materOt'):
        return "redirect"

    res = await getPropetry(item)

    return res


@materials.patch('/property/edit')
async def editProperty(property: EditProperty, request: Request):
    auth = request.cookies.get('Auth')

    if not auth:
        return "redirect"

    user = await isUsers(request)

    if not user.get('materOt'):
        return "redirect"

    res = await editPropetry(property.unitname, property.datestart, property.cost, property.costyear, property.costafter, property.period, property.hallid, int(property.unitid))


@materials.delete('/property/delete')
async def deleteProperty(property: PropertyDelete, request: Request):
    auth = request.cookies.get('Auth')

    if not auth:
        return "redirect"

    user = await isUsers(request)

    if not user.get('materOt'):
        return "redirect"

    res = await deletePropetry(int(property.unitid))

    if not res:
        return JSONResponse(
            content={'message': 'Ошибка'},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return

@materials.get('/building')
async def building(request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return RedirectResponse('/login')

    user = await isUsers(request)
    if not user.get('materOt'):
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
    
    return template.TemplateResponse('financiallyResponsible/building.j2', {'request': request, 'emu': new_emu})