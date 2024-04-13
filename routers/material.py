from fastapi import APIRouter, status
from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from pydantic import BaseModel
from database.connection import *
from typing import Union
from datetime import datetime
import base64

template = Jinja2Templates(directory='resources/views')

materials = APIRouter(
    prefix='/materil',
    tags=['materials']
)


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


@materials.get('/building/edit/{id}')
async def editBuilding(id: Union[str, int], request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return "redirect"
    user = await isUsers(request)
    if not user.get('materOt'):
        return "redirect"

    res = await getOneBuilding(id)

    id_build, id_kadastr, buildingname, land, material, wear, flow, comment = res

    return {
        'id': id_build,
        'kadastr': id_kadastr,
        'buildingname': buildingname,
        'land': land,
        'material': material,
        'wear': wear,
        'flow': flow,
        'comment': comment
    }


class EditBuilding(BaseModel):
    buildingname: str
    land: str
    material: str
    wear: str
    flow: str
    comment: str
    id_kadastr: str
    id_building: Union[str, int]


@materials.patch('/building/edit')
async def editBuildings(building: EditBuilding, request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return "redirect"
    user = await isUsers(request)
    if not user.get('materOt'):
        return "redirect"
    res = await editBuildingst(building.id_building, building.buildingname, building.land, building.material, building.wear, building.flow, building.comment, building.id_kadastr)
    return


class BuildingCreate(BaseModel):
    buildingname: str
    land: str
    material: str
    wear: str
    flow: str
    comment: str
    id_kadastr: str


@materials.post('/building/create')
async def createBuildings(building: BuildingCreate, request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return "redirect"
    user = await isUsers(request)
    if not user.get('materOt'):
        return "redirect"

    res = await createBuilding(building.buildingname, building.land, building.material, building.wear, building.flow, building.comment, building.id_kadastr)

    return


class BuildingDelete(BaseModel):
    id_building: Union[str, int]


@materials.delete('/building/delete')
async def deleteBuildingS(item: BuildingDelete, request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return "redirect"
    user = await isUsers(request)
    if not user.get('materOt'):
        return "redirect"
    res = await deleteBuilding(int(item.id_building))
    return


@materials.get('/kadastr')
async def kadastr(request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return "redirect"
    user = await isUsers(request)
    if not user.get('materOt'):
        return "redirect"
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

    return template.TemplateResponse('financiallyResponsible/kadastr.j2', {'request': request, 'emu': new_emu})


@materials.get('/kadastr/edit/{id}')
async def editKadastr(id: Union[str, int], request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return "redirect"
    user = await isUsers(request)
    if not user.get('materOt'):
        return "redirect"
    res = await getOneKadastr(id)
    id_kadastr, street, house, year = res
    return {
        'id': id_kadastr,
        'street': street,
        'house': house,
        'year': year
    }


class EditKadastr(BaseModel):
    id_kadastr: str
    street: str
    house: str
    year: str


@materials.patch('/kadastr/edit')
async def editKadastrs(kadastr: EditKadastr, request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return RedirectResponse('/login')
    user = await isUsers(request)
    if not user.get('materOt'):
        return RedirectResponse('/login')
    res = await editKadastrsOne(kadastr.id_kadastr, kadastr.street, kadastr.house, kadastr.year)
    return

class CreateKadastr(BaseModel):
    id: str
    street: str
    house: str
    year: str

@materials.post('/kadastr/create')
async def createKadastr(kadastr: CreateKadastr, request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return "redirect"
    user = await isUsers(request)
    if not user.get('materOt'):
        return "redirect"
    res = await createKadastrs(kadastr.id, kadastr.street, kadastr.house, kadastr.year)
    return


@materials.delete('/kadastr/delete/{item}')
async def deleteKadastr(item: str, request: Request):
    auth = request.cookies.get('Auth')

    if not auth:
        return "redirect"

    users = await isUsers(request)

    if not users.get('materOt'):
        return "redirect"

    res = await deleteKadastrs(item)

    return res

@materials.get('/images')
async def images(request: Request):
    auth = request.cookies.get('Auth')
    if not auth:
        return "redirect"
    user = await isUsers(request)
    if not user.get('materOt'):
        return "redirect"
    emu = await selectImages()
    if not emu:
        emu = []
    new_emu = []
    for i in emu:
        id, id_building, path = i
        new_emu.append({
            'id': id,
            'id_building': id_building,
            'photo': base64.b64encode(path).decode('utf-8')
        })
    return template.TemplateResponse('financiallyResponsible/images.j2', {'request': request, 'emu': new_emu})