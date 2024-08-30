import uvicorn
from fastapi import FastAPI, Request, HTTPException, APIRouter, Form
from starlette.templating import Jinja2Templates
from typing import Annotated

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
    return templates.TemplateResponse("type_records/type_record.html", {'request': request})


@router.get("/type_records/select_specialist")
async def select_specialist(request: Request):
    return templates.TemplateResponse("type_records/select_specialist.html", {'request': request})


@router.get("/type_records/select_services")
async def select_services(request: Request):
    return templates.TemplateResponse("type_records/select_services.html", {'request': request})


@router.get("/type_records/select_datetime")
async def select_datetime(request: Request):
    return templates.TemplateResponse("type_records/select_datatime.html", {'request': request})


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
