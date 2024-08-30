import uvicorn
from fastapi import FastAPI, Request, HTTPException, APIRouter, Form
from starlette.templating import Jinja2Templates
from typing import Annotated
from starlette.responses import RedirectResponse

app = FastAPI(
    title='Yclients'
)

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

data = {}


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})


@router.get("/type_records")
async def type_records(request: Request):
    return templates.TemplateResponse("type_record.html", {'request': request})


# Запись на событие по специалисту
@router.get("/type_records/select_specialist")
async def select_specialist(request: Request):
    return templates.TemplateResponse("specialist/select_specialist.html", {'request': request})


@router.get("/type_records/select_specialist/select_service")
async def select_service_for_specialist(request: Request):
    return templates.TemplateResponse("specialist/select_services.html", {'request': request})


@router.get("/type_records/select_specialist/select_service/select_date")
async def select_date_for_specialist(request: Request):
    return templates.TemplateResponse("specialist/select_datatime.html", {'request': request})


@router.post("/type_records/select_specialist/select_service/select_date")
async def select_date_for_specialist(request: Request, date: Annotated[str, Form()], time: Annotated[str, Form()]):
    redirect_url = request.url_for("success_for_specialist")
    return RedirectResponse(redirect_url)


@router.get("/type_records/select_specialist/select_service/select_date/success")
async def success_for_specialist(request: Request):
    return templates.TemplateResponse("specialist/success.html", {'request': request})


@router.post("/type_records/select_specialist/select_service/select_date/success")
async def success_for_specialist(request: Request):
    return templates.TemplateResponse("specialist/success.html", {'request': request})


# Запись на событие по услуге
@router.get("/type_records/select_service")
async def select_services(request: Request):
    return templates.TemplateResponse("services/select_service.html", {'request': request})


@router.get("/type_records/select_service/select_specialist")
async def select_specialist_for_services(request: Request):
    return templates.TemplateResponse("services/select_specialist.html", {'request': request})


@router.get("/type_records/select_service/select_specialist/select_date")
async def select_date_for_services(request: Request):
    return templates.TemplateResponse("services/select_date.html", {'request': request})


@router.post("/type_records/select_service/select_specialist/select_date")
async def select_date_for_services(request: Request, date: Annotated[str, Form()], time: Annotated[str, Form()]):
    redirect_url = request.url_for("select_success_for_services")
    return RedirectResponse(redirect_url)


@router.get("/type_records/select_service/select_specialist/select_date/success")
async def select_success_for_services(request: Request):
    return templates.TemplateResponse("services/success.html", {'request': request})


@router.post("/type_records/select_service/select_specialist/select_date/success")
async def select_success_for_services(request: Request):
    return templates.TemplateResponse("services/success.html", {'request': request})


# Запись на событие по дате
@router.get("/type_records/select_date")
async def select_datetime(request: Request):
    return templates.TemplateResponse("date/select_date.html", {'request': request})


@router.post("/type_records/select_date")
async def select_datetime(request: Request, date: Annotated[str, Form()], time: Annotated[str, Form()]):
    redirect_url = request.url_for("select_service_for_date")
    return RedirectResponse(redirect_url)


@router.get("/type_records/select_date/select_service")
async def select_service_for_date(request: Request):
    return templates.TemplateResponse("date/select_service.html", {'request': request})


@router.post("/type_records/select_date/select_service")
async def select_service_for_date(request: Request):
    return templates.TemplateResponse("date/select_service.html", {'request': request})


@router.get("/type_records/select_date/select_service/select_specialist")
async def select_specialist_for_date(request: Request):
    return templates.TemplateResponse("date/select_specialist.html", {'request': request})


@router.get("/type_records/select_date/select_service/select_specialist/success")
async def select_success_for_date(request: Request):
    return templates.TemplateResponse("date/success.html", {'request': request})


@router.get("/records")
async def recording(request: Request):
    return templates.TemplateResponse("recording/record.html", {'request': request})


@router.post("/records")
async def recording(request: Request, record_select: Annotated[str, Form()], date: Annotated[str, Form()],
                    human_select: Annotated[str, Form()], name: Annotated[str, Form()], phone: Annotated[str, Form()],
                    email: Annotated[str, Form()] | None = "", comment: Annotated[str, Form()] | None = ""):
    return templates.TemplateResponse("recording/record_answer.html", {'request': request})


app.include_router(router)


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


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
