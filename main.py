import uvicorn

from fastapi import FastAPI, Request, HTTPException, APIRouter, Form
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from app.routers.schemas import ServicesLoad
from app.routers.services import router as services_router
from app.routers.group_services import router as groups_router
from conf import YclientsConfig
from yclients.yclient import Yclient

app = FastAPI(
    title='Services API',
)

router = APIRouter(
    prefix='/book_record',
    tags=['Book record']
)

templates = Jinja2Templates(directory="app/templates")

yclient = YclientsConfig()
api = Yclient(bearer_token=yclient.bearer, company_id=yclient.company_id, user_token=yclient.user)


@app.get("/")
async def index(request: Request):
    redirect_url = request.url_for('home')
    return RedirectResponse(redirect_url)


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})


@router.get("/get_services", response_model=ServicesLoad)
async def get_services():
    exist = True
    services = await api.book_services()
    if services is None:
        exist = False
    return {"exist": exist}


@router.get("/get_services_group", response_model=ServicesLoad)
async def get_services_group():
    exist = True
    group_services = await api.dates_range()
    if group_services is None:
        exist = False
    return {"exist": exist}


@router.get("/health")
async def health():
    return {'status_code': 200}


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


if __name__ == '__main__':
    uvicorn.run('main:app')
