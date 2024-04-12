from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from database.connection import *
from typing import List, Dict
from pydantic import BaseModel

# routers
from routers.material import materials


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

    auth = request.cookies.get('Auth')

    if auth:
        res = await isUsers(request=request)

        if res.get('admin'):
            return RedirectResponse('/admin')
        elif res.get('materOt'):
            return RedirectResponse('/materil')
        elif res.get('user'):
            return RedirectResponse('/user')
                

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

    return {
        "id": res.get("id"),
        "role": res.get("role")
    }


@app.get('/admin')
async def admin(request: Request):
    auth = request.cookies.get('Auth')
    
    if not auth:
        return RedirectResponse('/')
    
    res = await isUsers(request)

    if not res.get('admin'):
        return RedirectResponse('/')

    return tempalte.TemplateResponse("admin/index.j2", {"request": request})

@app.get('/logout')
async def logout(request: Request, response: Response):

    response.delete_cookie("Auth")
    response.delete_cookie("id")

    
    return

app.include_router(materials)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', reload=True)
