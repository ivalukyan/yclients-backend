"""
Services
"""
from fastapi import APIRouter, Request, Form
from httptools.parser.parser import HttpRequestParser
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from typing import Annotated
from uuid import uuid4
from app.routers.utils import get_times, get_hash

from yclients.yclient import Yclient
from conf import YclientsConfig

from app.routers.schemas import Dates, Times, SaveTime, UserData


router = APIRouter(
    prefix="/book_record/services",
    tags=["Services"]
)

yclient = YclientsConfig()
api = Yclient(bearer_token=yclient.bearer, company_id=yclient.company_id, user_token=yclient.user)

templates = Jinja2Templates(directory="app/templates")

cache_ = {}
user_id = 877008114


# Запись на Индивидульные занятия
@router.get("/")
async def book_services(request: Request):
    """Получние доступных услуг для бронирования"""

    services = await api.book_services()
    user_hash = await get_hash(str(user_id))

    if not services:
        exp = "Услуги для бронирования отсутствуют"
        return templates.TemplateResponse("booking/services.html", {'request': request, 'exp': exp})
    else:
        return templates.TemplateResponse("booking/services.html", {'request': request,
                                                                    'data': services.values(),
                                                                    'user_id': user_id})


@router.get("/{service_id}")
async def book_staff(request: Request, service_id: int):
    """Получение персонала по выбранной услуге"""

    staff = await api.book_staff()

    return templates.TemplateResponse("booking/staffs.html",
                                      {'request': request, 'data': staff.values(), 'service_id': service_id})


@router.post("/{service_id}")
async def book_staff(request: Request, service_id: int):

    redirect_url = request.url_for('book_created')
    return RedirectResponse(redirect_url)


@router.get("/{service_id}/{staff_id}")
async def book_date(request: Request, service_id: int, staff_id: int):
    """Получение доступных дат для записи"""

    dates = await api.book_dates()

    return templates.TemplateResponse("booking/dates.html",
                                      {'request': request, 'service_id': service_id, 'staff_id': staff_id,
                                       'data': dates.values()})


@router.post("/{service_id}/date", response_model=Dates)
async def save_reserve_date(date: Dates):
    """Сохранение выбранной даты для пользователя"""

    content = f"{date.staff_id} -- {date.date_id}"
    print(content)

    return {'date_id': date.date_id, 'staff_id': date.staff_id, 'content': content, 'status': 'ok', 'msg': 'Save date'}


@router.post("/{service_id}/times", response_model=Times)
async def get_reserve_times(time: Times):
    """Получение доступных времен для выбранной даты"""

    times = await api.book_times(staff_id=time.staff_id, date=time.select_date)
    available_times = await get_times(times.values())
    content = f"{time.staff_id} -- {time.select_date}"
    print(content)

    return {'available_times': available_times, 'select_date': time.select_date, 'staff_id': time.staff_id,
            'content': content, 'status': 'ok', 'msg': 'Get times'}


@router.post("/{service_id}/save", response_model=SaveTime)
async def save_reserve_times(request: Request, time: SaveTime):
    """Сохранение полученных даты и времени"""

    content = f"Выбранное время: {time.save_time}, Выбранная дата: {time.save_date}"
    print(content)

    return {'save_time': time.save_time, 'save_date': time.save_date,
            'content': content, 'status': 'ok', 'msg': 'Save time'}


@router.get("/{service_id}/{staff_id}/recording")
async def book_created(request: Request, service_id: int, staff_id: int):
    """Создание онлайн-записи"""

    return templates.TemplateResponse("booking/recording.html", {'request': request,
                                                                 'service_id': service_id,
                                                                 'staff_id': staff_id})


@router.post("/{service_id}/{staff_id}/recording", response_model=UserData)
async def book_created(request: Request, service_id: int, staff_id: int, user: UserData):
    """Создание онлай-записи"""

    print(user)

    return templates.TemplateResponse("booking/recording.html", {'request': request,
                                                                 'service_id': service_id,
                                                                 'staff_id': staff_id})


@router.get('/{service_id}/{staff_id}/success')
async def success(request: Request, service_id: int, staff_id: int):
    return templates.TemplateResponse('booking/success.html', {'request': request,
                                                               'staff_id': staff_id,
                                                               'service_id': service_id})

