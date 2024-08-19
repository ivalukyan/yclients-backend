import uvicorn
from fastapi import FastAPI, Request, HTTPException
from starlette.templating import Jinja2Templates

app = FastAPI(
    title='Yclients'
)

templates = Jinja2Templates(directory="backend/app/templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("recording/home.html", {'request': request})


@app.exception_handler(404)
async def custom_404_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("exception_handler/404.html", {"request": request, 'exception': exp})


@app.exception_handler(500)
async def custom_500_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("exception_handler/500.html", {"request": request, 'exception': exp})


@app.exception_handler(400)
async def custom_400_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("exception_handler/400.html", {"request": request, 'exception': exp})


@app.exception_handler(405)
async def custom_405_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("exception_handler/405.html", {"request": request, 'exception': exp})
