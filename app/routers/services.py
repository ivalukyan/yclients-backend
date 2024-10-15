"""
Services
"""

import logging

from fastapi import APIRouter, Request, Form
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from typing import Annotated

from yclients.yclient import Yclient
from conf import YclientsConfig

from app.routers.schemas import Dates, Times

router = APIRouter(
    prefix="/book_record/services",
    tags=["Services"]
)

yclient = YclientsConfig()
api = Yclient(bearer_token=yclient.bearer, company_id=yclient.company_id, user_token=yclient.user)

templates = Jinja2Templates(directory="app/templates")

# Запись на Индивидульные занятия
@router.get("/")
async def book_services(request: Request):
    """Получние доступных услуг для бронирования"""

    services = await api.book_services()

    if not services:
        exp = "Услуги для бронирования отсутствуют"
        return templates.TemplateResponse("booking/services.html", {'request': request, 'exp': exp})
    else:
        return templates.TemplateResponse("booking/services.html", {'request': request, 'data': services.values()})


@router.get("/{service_id}")
async def book_staff(request: Request, service_id: int):
    """Получение персонала по выбранной услуге"""

    staff = await api.book_staff()

    return templates.TemplateResponse("booking/staffs.html",
                                      {'request': request, 'data': staff.values(), 'service_id': service_id})


@router.get("/{service_id}/{staff_id}")
async def book_date(request: Request, service_id: int, staff_id: int):
    """Получение доступных дат для записи"""

    dates = await api.book_dates()

    return templates.TemplateResponse("booking/dates.html",
                                      {'request': request, 'service_id': service_id, 'staff_id': staff_id,
                                       'data': dates.values()})


@router.post("/reserve/date")
async def save_reserve_date(date: Annotated[str, Form]):
    """Сохранение выбранной даты для пользователя"""

    print("Выбранная дата: ", date)

    return {"select_date": date, "status": "ok", "mes": "Дата выбрана"}


@router.post("/reserve/times", response_model=Times)
async def get_reserve_times(times: Times):
    """Получение доступных времен для выбранной даты"""

    times = await api.book_times(staff_id=times.staff_id, date=times.date)
    print(times.values())

    return {'date': times.values()}


@router.get("/{service_id}/{staff_id}/{date_id}")
async def book_time(request: Request, service_id: int, staff_id: int, date_id: str):
    """Получение доступного времени для записи"""

    times = await api.book_times(staff_id=staff_id, date=date_id)

    return templates.TemplateResponse("booking/times.html",
                                      {'request': request, 'service_id': service_id, 'staff_id': staff_id,
                                       'date': date_id,
                                       'data': times.values()})


@router.get("{service_id}/{staff_id}/{date_id}/{time_id}")
async def book_created(request: Request, service_id: int, staff_id: int, date_id: str, time_id: str):
    """Создание онлайн-записи"""

    return templates.TemplateResponse("booking/recording.html",
                                      {'request': request, 'service_id': service_id, 'staff_id': staff_id,
                                       'date_id': date_id, 'time_id': time_id})


@router.post("/{service_id}/{staff_id}/{date_id}/{time_id}")
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
        return templates.TemplateResponse("booking/recording.html",
                                          {'request': request, 'service_id': service_id, 'staff_id': staff_id,
                                           'date_id': date_id, 'time_id': time_id, 'exp': record['meta']['message']})

