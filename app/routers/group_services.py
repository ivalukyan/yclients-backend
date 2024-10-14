"""
Group services
"""

from fastapi import APIRouter, Request, Form
from starlette.templating import Jinja2Templates
from typing import Annotated
from starlette.responses import RedirectResponse

from yclients.yclient import Yclient
from conf import YclientsConfig


router = APIRouter(
    prefix="/book_record/group_services",
    tags=["Group services"],
)

yclient = YclientsConfig()
api = Yclient(bearer_token=yclient.bearer, company_id=yclient.company_id, user_token=yclient.user)

templates = Jinja2Templates(directory="app/templates")


# Запись на груповые события
@router.get("/")
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
            return templates.TemplateResponse("booking/group_services.html",
                                              {'request': request, 'data': group_services})


@router.get("/{service_id}")
async def recording_group_services(request: Request, service_id: int):
    return templates.TemplateResponse("booking/recording.html", {'request': request, 'service_id': service_id})


@router.post("/{service_id}")
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
        return templates.TemplateResponse("booking/recording.html",
                                          {'request': request, 'service_id': service_id, 'staff_id': staff_id,
                                           'date_id': date_id, 'time_id': time_id,
                                           'exp': group_record['meta']['message']})
