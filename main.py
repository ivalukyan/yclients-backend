import uvicorn
from fastapi import FastAPI, Request, HTTPException, APIRouter, Form
from starlette.templating import Jinja2Templates
from typing import Annotated
from starlette.responses import RedirectResponse
from yclients.yclient import Yclient
from conf import YclientsConfig

app = FastAPI(
    title='Yclients'
)

router = APIRouter()
yclient = YclientsConfig()
api = Yclient(bearer_token=yclient.bearer, company_id=yclient.company_id, user_token=yclient.user)

templates = Jinja2Templates(directory="app/templates")



@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})


@router.get("/health")
async def health():
    return {'status_code': 200}

# Запись на груповые события
@router.get("/book_record/group_services")
async def group_services(request: Request):
    """Получение групповых событий"""

    date = await api.dates_range()

    if not date:
        exp = "Групповые события отсутствуют"
        return templates.TemplateResponse("booking/group_services.html", {'request': request, 'exp': exp})
    else:
        if date['min_date'] is None and date['max_date'] is None:
            exp = "Групповые события отсутствуют"
            return templates.TemplateResponse("booking/group_services.html", {'request': request, 'exp': exp})
        else:
            group_services = await api.activity(from_date=date['min_date'], till_date=date['max_date'])
            return templates.TemplateResponse("booking/group_services.html", {'request': request, 'data': group_services})


@router.get("/book_record/group_services/{service_id}")
async def recording_group_services(request: Request, service_id: int):
    return templates.TemplateResponse("booking/recording.html", {'request': request, 'service_id': service_id})


@router.post("/book_record/services/{service_id}")
async def book_created(request: Request, service_id: int, staff_id: int, date_id: str, time_id: str,
                       name: Annotated[str, Form()], phone: Annotated[str, Form()], email: Annotated[str, Form()] = "",
                       comment: Annotated[str, Form()] = ""):
    """Создание онлай-записи"""
    
    group_record = await api.create_group_booking(activity_id=service_id, fullname=name, phone=phone, email=email,
                                                  comment=comment)
    

    if group_record['success']:
        redirect_url = request.url_for("success")
        return RedirectResponse(redirect_url)
    else:
        return templates.TemplateResponse("booking/recording.html", {'request': request, 'service_id': service_id, 'staff_id': staff_id,
                                                                  'date_id': date_id, 'time_id': time_id, 'exp': group_record['meta']['message']})


@router.get("/book_record/success")
async def success(request: Request):
    """Страница подтверждающая запись"""

    return templates.TemplateResponse("booking/success.html", {'request': request})


@router.post("/book_record/success")
async def success(request: Request):
    """Страница подтверждающая запись"""

    return templates.TemplateResponse("booking/success.html", {'request': request})


# Запись на Индивидульные занятия
@router.get("/book_record/services")
async def book_services(request: Request):
    """Получние доступных услуг для бронирования"""

    services = await api.book_services()
    print(services)

    if not services:
        exp = "Услуги для бронирования отсутствуют"
        return templates.TemplateResponse("booking/services.html", {'request': request, 'exp': exp})
    else:
        return templates.TemplateResponse("booking/services.html", {'request': request, 'data': services.values()})


@router.get("/book_record/services/{service_id}")
async def book_staff(request: Request, service_id: int):
    """Получение персонала по выбранной услуге"""

    staff = await api.book_staff()

    return templates.TemplateResponse("booking/staffs.html", {'request': request, 'data': staff.values(), 'service_id': service_id})


@router.get("/book_record/services/{service_id}/{staff_id}")
async def book_date(request: Request, service_id: int, staff_id: int):
    """Получение доступных дат для записи"""

    dates = await api.book_dates()

    return templates.TemplateResponse("booking/dates.html", {'request': request, 'service_id': service_id, 'staff_id': staff_id, 'data': dates.values()})


@router.get("/book_record/services/{service_id}/{staff_id}/{date_id}")
async def book_time(request: Request, service_id: int, staff_id: int, date_id: str):
    """Получение доступного времени для записи"""

    times = await api.book_times(staff_id=staff_id, date=date_id)

    return templates.TemplateResponse("booking/times.html", {'request': request, 'service_id':service_id, 'staff_id': staff_id, 'date': date_id,
                                                             'data': times.values()})


@router.get("/book_record/services/{service_id}/{staff_id}/{date_id}/{time_id}")
async def book_created(request: Request, service_id: int, staff_id: int, date_id: str, time_id: str):
    """Создание онлайн-записи"""

    return templates.TemplateResponse("booking/recording.html", {'request': request, 'service_id': service_id, 'staff_id': staff_id,
                                                                  'date_id': date_id, 'time_id': time_id})


@router.post("/book_record/services/{service_id}/{staff_id}/{date_id}/{time_id}")
async def book_created(request: Request, service_id: int, staff_id: int, date_id: str, time_id: str,
                       name: Annotated[str, Form()], phone: Annotated[str, Form()], email: Annotated[str, Form()] = "",
                       comment: Annotated[str, Form()] = ""):
    """Создание онлай-записи"""

    record = await api.create_booking(phone=phone, fullname=name, email=email, comment=comment, service_id=service_id,
                            staff_id=staff_id, date_id=date_id, time_id=time_id)
    

    if record['success']:
        redirect_url = request.url_for("success")
        return RedirectResponse(redirect_url)
    else:
        return templates.TemplateResponse("booking/recording.html", {'request': request, 'service_id': service_id, 'staff_id': staff_id,
                                                                  'date_id': date_id, 'time_id': time_id, 'exp': record['meta']['message']})


@router.get("/book_record/success")
async def success(request: Request):
    """Страница подтверждающая запись"""

    return templates.TemplateResponse("booking/success.html", {'request': request})


@router.post("/book_record/success")
async def success(request: Request):
    """Страница подтверждающая запись"""

    return templates.TemplateResponse("booking/success.html", {'request': request})


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