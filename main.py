from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from database.connection import *
from typing import List, Dict
from pydantic import BaseModel


def isUsers(request: Request) -> object:
    id = request.cookies.get('id')
    role = request.cookies.get('role').encode('utf-8')

    if not id or not role:
        return RedirectResponse('/login')

    if role == "Администратор":
        return {
            "admin": True,
            "materOt": False,
            "user": False
        }
    elif role == "Материально. отвественный":
        return {
            "admin": False,
            "materOt": True,
            "user": False
        }
    elif role == "Пользователь":
        return {
            "admin": False,
            "materOt": False,
            'user': True
        }


app = FastAPI()

tempalte = Jinja2Templates(directory="resources/views")

app.mount("/static", StaticFiles(directory="resources/"), name="resources")
app.mount("/public", StaticFiles(directory="public"), name="public")

app.add_middleware(
    CORSMiddleware,
    # This allows requests from all origins, you might want to specify specific origins
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],  # You can specify specific headers
)


@app.get("/")
async def index(request: Request):
    return RedirectResponse('/login')


@app.get('/login')
async def login(request: Request):
    return tempalte.TemplateResponse("login/login.j2", {"request": request})


class User(BaseModel):
    login: str
    password: str


@app.post('/login')
async def login(user: User, response: Response):
    res: Dict = await logins(user.login, user.password)

    print(res)

    if not res:
        return JSONResponse(content={"msg": "Invalid username or password"}, status_code=status.HTTP_401_UNAUTHORIZED)

    response.set_cookie(key="Auth", value="true")
    response.set_cookie(key="id", value=res.get("id"), httponly=True)
    response.set_cookie(key="role", value=res.get(
        "role").encode('utf-8'), httponly=True)

    return {
        "id": res.get("id"),
        "role": res.get("role")
    }


@app.get('/admin')
async def admin(request: Request):
    role_cookie = request.cookies.get('role')
    if isinstance(role_cookie, bytes):
        role = role_cookie.decode('utf-8')
        print(role)

    print(role_cookie)

    return tempalte.TemplateResponse("admin/index.j2", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', reload=True)
