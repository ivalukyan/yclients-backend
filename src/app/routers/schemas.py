"""
Schemas app
"""

from pydantic import BaseModel


class Times(BaseModel):
    staff_id: int
    select_date: str
    available_times: list

class Dates(BaseModel):
    staff_id: int
    service_ids: list


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
    success: bool | None = None
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


class BookStaffData(BaseModel):
    staff_id: int
    staff_name: str
    staff_specialization: str
    staff_avatar: str
    staff_info: str | None = None

    class Config:
        from_attributes = True