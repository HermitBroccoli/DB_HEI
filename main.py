from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

tempalte = Jinja2Templates(directory="resources/views")

app.mount("/static", StaticFiles(directory="resources/"), name="resources")
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/")
async def index(request: Request):
    return tempalte.TemplateResponse("index/index.html.j2", {"request": request})

@app.get('/login')
async def login(request: Request):
    return tempalte.TemplateResponse("login/login.html.j2", {"request": request})
                
if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', reload=True)