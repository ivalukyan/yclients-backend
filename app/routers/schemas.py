"""
Schemas app
"""

from pydantic import BaseModel


class Times(BaseModel):
    staff_id: int
    select_date: str
    available_times: list


class DataTime(BaseModel):
    user_id: int
    save_date: str
    save_time: str


class UserData(BaseModel):
    name: str
    phone: str
    email: str | None = None
    comment: str | None = None
    date_id: str
    time_id: str
    status: bool | None = None
    message: str | None = None


class ServiceSchemas(BaseModel):
    user_id: int
    fullname: str
    service_id: int
    staff_id: int


class FormData(BaseModel):
    user_id: int
    phone: str | None = None
    cache: dict[str, str] | None = None


class FormGroup(BaseModel):
    user_id: int
    phone: str


class SearchSchemas(BaseModel):
    text: str
    list_search: list


class ServicesLoad(BaseModel):
    exist: bool