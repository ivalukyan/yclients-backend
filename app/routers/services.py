"""
Services
"""
from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.routers.schemas import Times, DataTime, UserData, ServiceSchemas, FormData, Dates
from app.routers.utils import get_times, remove_html_tags, include_staffs
from conf import YclientsConfig
from db.utils import get_user_phone_number
from yclients.yclient import Yclient

router = APIRouter(
    prefix="/book_record/category",
    tags=["Services"]
)

yclient = YclientsConfig()
api = Yclient(bearer_token=yclient.bearer, company_id=yclient.company_id, user_token=yclient.user)

templates = Jinja2Templates(directory="app/templates")

cache_ = {}


# Запись на Индивидульные занятия
@router.get("/")
async def category_services(request: Request):
    """Получение категорий"""

    category = await api.book_category()

    if not category:
        exp = "Категории отсутствуют"
        return templates.TemplateResponse("booking/category_services.html", {'request': request, 'exp': exp})
    return templates.TemplateResponse("booking/category_services.html", {'request': request,
                                                                         'data': category.values()})


@router.get("/services")
async def book_services(request: Request):
    """Получние доступных услуг для бронирования"""

    services = await api.book_services()
    values = list(services.values())

    for i in values:
        i['service_description'] = await remove_html_tags(i['service_description'])

    if not services:
        exp = "Услуги для бронирования отсутствуют"
        return templates.TemplateResponse("booking/services.html", {'request': request, 'exp': exp})
    else:
        return templates.TemplateResponse("booking/services.html", {'request': request,
                                                                    'data': values})


@router.get("/services/{service_id}")
async def book_staff(request: Request, service_id: int):
    """Получение персонала по выбранной услуге"""


    service_staff_id= await api.get_staff(service_id)
    staff = await api.book_staff()

    staff_values = list(staff.values())

    data = await include_staffs(service_staff_id, staff_values)

    for i in data:
        i['staff_info'] = await remove_html_tags(i['staff_info'])

    return templates.TemplateResponse("booking/staffs.html",
                                      {'request': request, 'staffs': data,
                                       'service_id': service_id})


@router.post("/services/{service_id}", response_model=ServiceSchemas)
async def book_staff(user: ServiceSchemas):
    cache_[user.user_id] = {'fullname': user.fullname, 'service_id': str(user.service_id),
                            'staff_id': str(user.staff_id)}

    content = f"User: {user.user_id} -- Service: {user.service_id} -- Staff: {user.staff_id}"
    print(cache_)

    return {'fullname': user.fullname, 'staff_id': user.staff_id, 'user_id': user.user_id,
            'service_id': user.service_id, 'content': content,
            'status': 'ok', 'msg': 'Save service data'}


@router.get("/services/{service_id}/{staff_id}")
async def book_date(request: Request, service_id: int, staff_id: int):
    """Получение доступных дат для записи"""

    dates = await api.book_dates(service_ids=[service_id], staff_id=staff_id)
    # print(dates)
    # print('VALUES', dates.values())
    dates_formatted = [d['book_date'] for d in dates.values()]
    print('FORMATTED DATES', dates_formatted)

    return templates.TemplateResponse("booking/dates.html",
                                      {'request': request, 'service_id': service_id, 'staff_id': staff_id,
                                       'data': dates_formatted})


@router.post("/services/{service_id}/times", response_model=Times)
async def get_reserve_times(time: Times):
    """Получение доступных времен для выбранной даты"""

    times = await api.book_times(staff_id=time.staff_id, date=time.select_date)
    #print(times)
    if not times:
        available_times = []
    else:
        available_times = await get_times(times.values())
    #print(available_times)
    content = f"{time.staff_id} -- {time.select_date}"

    return {'available_times': available_times,
            'select_date': time.select_date, 'staff_id': time.staff_id,
            'content': content, 'status': 'ok', 'msg': 'Get times'}

@router.post("/services/{service_id}/dates", response_model=Dates)
async def get_reserve_dates(date: Dates):
    """Получение доступных дат для выбранного сотрудника и услуги"""

    dates = await api.book_dates(staff_id=date.staff_id, service_ids=date.service_ids)
    #print(times)
    if not dates:
        available_dates = []
    else:
        available_dates = await get_times(dates.values())
    #print(available_times)
    content = f"{date.staff_id} -- {date.service_ids}"

    return {'available_dates': available_dates,
            'select_service_ids': date.service_ids, 'staff_id': date.staff_id,
            'content': content, 'status': 'ok', 'msg': 'Get times'}


@router.post("/services/{service_id}/save", response_model=DataTime)
async def save_reserve_times(request: Request, datatime: DataTime):
    """Сохранение полученных даты и времени"""

    print(datatime.user_id)

    cache_[datatime.user_id]['date'] = datatime.save_date
    cache_[datatime.user_id]['time'] = datatime.save_time

    content = f"Выбранное время: {datatime.save_time}, Выбранная дата: {datatime.save_date}"

    return {'user_id': datatime.user_id, 'save_time': datatime.save_time, 'save_date': datatime.save_date,
            'content': content, 'status': 'ok', 'msg': 'Save time'}


@router.get("/services/{service_id}/{staff_id}/recording")
async def book_created(request: Request, service_id: int, staff_id: int):
    """Создание онлайн-записи"""

    print(cache_)
    return templates.TemplateResponse("booking/recording.html", {'request': request,
                                                                 'service_id': service_id,
                                                                 'staff_id': staff_id})


@router.post("/services/{service_id}/{staff_id}/get_form_data", response_model=FormData)
async def get_form_data(service_id: int, staff_id: int, form: FormData):

    phone = get_user_phone_number(form.user_id)
    print(phone)

    return {'cache': cache_[form.user_id], 'phone': phone,
            'user_id': form.user_id, 'content': f'{form.user_id}',
            'status': 'ok', 'msg': 'Get form data'}


@router.post("/services/{service_id}/{staff_id}/recording", response_model=UserData)
async def book_created(request: Request, service_id: int, staff_id: int, user: UserData):
    """Создание онлай-записи"""

    service = await api.create_booking(fullname=user.name, phone=user.phone, email=user.email,
                                 comment=user.comment, service_id=service_id, staff_id=staff_id,
                                 date_id=user.date_id, time_id=user.time_id)

    if service['success']:
        return UserData(name=user.name, phone=user.phone, date_id=user.date_id, time_id=user.time_id,
                        success=service['success'])
    else:
        return UserData(name=user.name, phone=user.phone, date_id=user.date_id, time_id=user.time_id,
                    success=service['success'], message=service['meta']['message'])


@router.get('/services/{service_id}/{staff_id}/success')
async def success(request: Request, service_id: int, staff_id: int):
    return templates.TemplateResponse('booking/success.html', {'request': request,
                                                               'staff_id': staff_id,
                                                               'service_id': service_id})


@router.post('/services/{service_id}/{staff_id}/success')
async def success(request: Request, service_id: int, staff_id: int):
    return templates.TemplateResponse('booking/success.html', {'request': request,
                                                               'staff_id': staff_id,
                                                               'service_id': service_id})




