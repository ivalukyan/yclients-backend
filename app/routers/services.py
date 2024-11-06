"""
Services
"""
from fastapi import APIRouter, Request, Form, HTTPException
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from typing import Annotated
from uuid import uuid4
from app.routers.utils import get_times, get_search, remove_html_tags

from yclients.yclient import Yclient
from conf import YclientsConfig

from app.routers.schemas import Times, DataTime, UserData, ServiceSchemas, FormData, SearchSchemas

from db.utils import get_user_phone_number


router = APIRouter(
    prefix="/book_record/services",
    tags=["Services"]
)

yclient = YclientsConfig()
api = Yclient(bearer_token=yclient.bearer, company_id=yclient.company_id, user_token=yclient.user)

templates = Jinja2Templates(directory="app/templates")

cache_ = {}


# Запись на Индивидульные занятия
@router.get("/")
async def book_services(request: Request):
    """Получние доступных услуг для бронирования"""

    services = await api.book_services()
    print(services)
    values = list(services.values())
    for i in values:
        i['service_description'] = await remove_html_tags(i['service_description'])

    print(values)
    if not services:
        exp = "Услуги для бронирования отсутствуют"
        return templates.TemplateResponse("booking/services.html", {'request': request, 'exp': exp})
    else:
        return templates.TemplateResponse("booking/services.html", {'request': request,
                                                                    'data': values})


@router.get("/category")
async def category_services(request: Request):
    """Получение категорий"""

    category = await api.book_category()
    print(category)

    if not category:
        exp = "Категории отсутствуют"
        return templates.TemplateResponse("booking/category_services.html", {'request': request, 'exp': exp})
    return templates.TemplateResponse("booking/category_services.html", {'request': request,
                                                                         'data': category.values()})


@router.post('/search', response_model=SearchSchemas)
async def get_search_services(search: SearchSchemas):

    list_services = await api.book_services()
    search_service = await get_search(search.text, list_services.values(), 'service_title')

    return {'text': search.text, 'list_search': search_service,
            'content': f"{search.text}", 'status': 'ok', 'msg': 'Search services'}


@router.get("/{service_id}")
async def book_staff(request: Request, service_id: int):
    """Получение персонала по выбранной услуге"""

    staff = await api.book_staff()
    values = list(staff.values())
    for i in values:
        i['staff_info'] = await remove_html_tags(i['staff_info'])

    return templates.TemplateResponse("booking/staffs.html",
                                      {'request': request, 'data': values, 'service_id': service_id})


@router.post("/{service_id}", response_model=ServiceSchemas)
async def book_staff(user: ServiceSchemas):
    cache_[user.user_id] = {'fullname': user.fullname, 'service_id': str(user.service_id),
                            'staff_id': str(user.staff_id)}

    content = f"User: {user.user_id} -- Service: {user.service_id} -- Staff: {user.staff_id}"
    print(cache_)

    return {'fullname': user.fullname, 'staff_id': user.staff_id, 'user_id': user.user_id,
            'service_id': user.service_id, 'content': content,
            'status': 'ok', 'msg': 'Save service data'}


@router.post('/{service_id}/search', response_model=SearchSchemas)
async def get_search_staffs(search: SearchSchemas):
    staff = await api.book_staff()

    list_staff = await get_search(search.text, staff.values(), 'staff_name')

    return {'text': search.text, 'list_search': list_staff,
            'content': f"{search.text}", 'status': 'ok', 'msg': 'Search staff'}


@router.get("/{service_id}/{staff_id}")
async def book_date(request: Request, service_id: int, staff_id: int):
    """Получение доступных дат для записи"""

    dates = await api.book_dates()

    return templates.TemplateResponse("booking/dates.html",
                                      {'request': request, 'service_id': service_id, 'staff_id': staff_id,
                                       'data': dates.values()})


@router.post("/{service_id}/times", response_model=Times)
async def get_reserve_times(time: Times):
    """Получение доступных времен для выбранной даты"""

    times = await api.book_times(staff_id=time.staff_id, date=time.select_date)
    print(times)
    if not times:
        available_times = []
    else:
        available_times = await get_times(times.values())
    print(available_times)
    content = f"{time.staff_id} -- {time.select_date}"

    return {'available_times': available_times,
            'select_date': time.select_date, 'staff_id': time.staff_id,
            'content': content, 'status': 'ok', 'msg': 'Get times'}


@router.post("/{service_id}/save", response_model=DataTime)
async def save_reserve_times(request: Request, datatime: DataTime):
    """Сохранение полученных даты и времени"""

    cache_[datatime.user_id]['date'] = datatime.save_date
    cache_[datatime.user_id]['time'] = datatime.save_time

    content = f"Выбранное время: {datatime.save_time}, Выбранная дата: {datatime.save_date}"

    return {'user_id': datatime.user_id, 'save_time': datatime.save_time, 'save_date': datatime.save_date,
            'content': content, 'status': 'ok', 'msg': 'Save time'}


@router.get("/{service_id}/{staff_id}/recording")
async def book_created(request: Request, service_id: int, staff_id: int):
    """Создание онлайн-записи"""

    return templates.TemplateResponse("booking/recording.html", {'request': request,
                                                                 'service_id': service_id,
                                                                 'staff_id': staff_id})


@router.post("/{service_id}/{staff_id}/get_form_data", response_model=FormData)
async def get_form_data(service_id: int, staff_id: int, form: FormData):

    phone = get_user_phone_number(form.user_id)
    print(phone)

    return {'cache': cache_[form.user_id], 'phone': phone,
            'user_id': form.user_id, 'content': f'{form.user_id}',
            'status': 'ok', 'msg': 'Get form data'}


@router.post("/{service_id}/{staff_id}/recording", response_model=UserData)
async def book_created(request: Request, service_id: int, staff_id: int, user: UserData):
    """Создание онлай-записи"""

    service = await api.create_booking(fullname=user.name, phone=user.phone, email=user.email,
                                 comment=user.comment, service_id=service_id, staff_id=staff_id,
                                 date_id=user.date_id, time_id=user.time_id)
    if service['success']:
        print('Запись сделана')
        redirect_url = request.url_for('success', service_id=service_id, staff_id=staff_id)
        return RedirectResponse(redirect_url)
    else:
        return templates.TemplateResponse("booking/recording.html", {'request': request,
                                                                 'service_id': service_id,
                                                                 'staff_id': staff_id})


@router.get('/{service_id}/{staff_id}/success')
async def success(request: Request, service_id: int, staff_id: int):
    return templates.TemplateResponse('booking/success.html', {'request': request,
                                                               'staff_id': staff_id,
                                                               'service_id': service_id})


@router.post('/{service_id}/{staff_id}/success')
async def success(request: Request, service_id: int, staff_id: int):
    return templates.TemplateResponse('booking/success.html', {'request': request,
                                                               'staff_id': staff_id,
                                                               'service_id': service_id})




