import uvicorn
from fastapi import FastAPI, Request, HTTPException, APIRouter, Form
from starlette.templating import Jinja2Templates

from app.routers.services import router as services_router
from app.routers.group_services import router as groups_router


app = FastAPI(
    title='Services API',
)

router = APIRouter(
    prefix='/book_record',
    tags=['Book record']
)

templates = Jinja2Templates(directory="app/templates")



@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})


@router.get("/health")
async def health():
    return {'status_code': 200}


@router.get("/success")
async def success(request: Request):
    """Страница подтверждающая запись"""

    return templates.TemplateResponse("booking/success.html", {'request': request})


app.include_router(router)
app.include_router(services_router)
app.include_router(groups_router)


@app.exception_handler(404)
async def custom_404_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("exception_handler/404.html", {"request": request, 'exception': exp})


@app.exception_handler(500)
async def custom_500_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("exception_handler/500.html", {"request": request, 'exception': exp})


@app.exception_handler(400)
async def custom_400_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("exception_handler/400.html", {"request": request, 'exception': exp})