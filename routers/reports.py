from fastapi import APIRouter, HTTPException, status
from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel
from database.connection import *
from typing import Union
from datetime import datetime
from subprocess import run
from jinja2 import Template
import re
import os

reports = APIRouter(
    tags=["Reports"]
)

templates = """

<!DOCTYPE html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>

    <style>
        * {
            padding: 0;
            margin: 0;
            box-sizing: border-box;
        }
    </style>
</head>

<body>

    <h1>
        Отчет по зданию «{{ nameBuilding }}» от {{ title }}
    </h1>

    <div style="width: 100%; display: flex; align-items: flex-start; justify-content: space-between;">
        <div class="params">
            <ul>
                <li>Дом: {{ nameBuilding }}</li>
                <li>Адрес: д. {{ address.street }} д. {{ address.house }}</li>
                <li>Год постройки: {{ address.year }}</li>
                <li>Число этажей: flow</li>
                <li>Материал: {{ material }}</li>
                <li>Площдь земельного участка: {{ land }}</li>
                <li>Процент износа: {{ wear }}</li>
                <li>Комментарий: {{ comment }}</li>
            </ul>
        </div>
        <div class="photo">
            <img src="{{photo}}" alt="photo">
        </div>
    </div>

    <h2>Кабинеты в данном здании</h2>

    <table style="border: 1px solid black; width: 100%;">

        <thead style="border: 1px solid black;">

            <tr style="border: 1px solid black;">
                <th style="border: 1px solid black; padding: 5px;">Номер кабинета</th>
                <th style="border: 1px solid black; padding: 5px;">Количество окон</th>
                <th style="border: 1px solid black; padding: 5px;">Площадь</th>
                <th style="border: 1px solid black; padding: 5px;">Число элементов в батареях отопления</th>
                <th style="border: 1px solid black; padding: 5px;">Комментарий</th>
            </tr>

        </thead>

        <tbody style="border: 1px solid black;">
            {% for item in hall %}
            <tr style="border: 1px solid black;">
                <td style="border: 1px solid black; padding: 5px;">{{ item.number }}</td>
                <td style="border: 1px solid black; padding: 5px;">{{ item.windows }}</td>
                <td style="border: 1px solid black; padding: 5px;">{{ item.square }}</td>
                <td style="border: 1px solid black; padding: 5px;">{{ item.heating }}</td>
                <td style="border: 1px solid black; padding: 5px;">{{ item.target }}</td>
            </tr>
            {% endfor %}
        </tbody>

    </table>

</body>

</html>

    """


@reports.get("/materil/report/build/{item}")
async def build_report(item: Union[str, int], request: Request):
    auth = request.cookies.get("Auth")
    if not auth:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Not authenticated"})

    res = await getBuildall(item)

    if not res:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Not found"})

    id, id_kadastr, buildingname, land, material, wear, flow, comment = res
    ids, street, house, year = await getOneKadastr(id_kadastr)
    res_img = await getOnePhotoBuilding(id)

    if res_img:
        photo_id, id_build, photo = res_img
    else:
        photo = ""

    hall_all = await getHallBuilding(id)
    new_hall = []

    title = datetime.now()
    safe_title = re.sub(r'[\\/*?:"<>|]', '_', str(title))

    for i in hall_all:
        hall_id, square, windows, heating, target, building_id, departament, mateterial_ot = i
        new_hall.append({
            "number": hall_id,
            "square": square,
            "windows": windows,
            "heating": heating,
            "target": target,
        })

    data = {
        "title": title,
        "nameBuilding": buildingname,
        "address": {
            "street": street,
            "house": house,
            "year": year,
        },
        "land": land,
        "material": material,
        "wear": wear,
        "flow": flow,
        "comment": comment,
        "photo": f"../resources/img/building/{photo}",
        "hall": new_hall
    }

    html = Template(templates)
    out_html = html.render(data)

    filename = f"{safe_title}.pdf"

    try:
        with open(f"temp/{safe_title}.html", "w", encoding="utf-8") as f:
            f.write(out_html)

        with open(f"temp/{safe_title}.html", "rb") as f:
            html_content = f.read()

        try:
            run(["wkhtmltopdf", '--enable-local-file-access', "--quiet", "--disable-javascript", "-",
                 f"temp/{safe_title}.pdf"], input=html_content, check=True)
        except:
            pass

        file_path = os.path.abspath(f"temp/{filename}")

        if os.path.exists(file_path):
            return FileResponse(file_path, headers={"Content-Disposition": f"attachment; filename={filename}"})
        else:
            return {"error": "File not found"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Remove the temporary HTML file
        os.remove(f"temp/{safe_title}.html")


@reports.get("/materil/report/download/{item}")
async def download_report(item: str, request: Request):
    auth = request.cookies.get("Auth")
    if not auth:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Not authenticated"})
    path = f"temp/{item}"

    if os.path.exists(path):
        return FileResponse(path=path)
    else:
        return {"error": "File not found"}
