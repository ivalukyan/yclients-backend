"""
Schemas app
"""

from pydantic import BaseModel


class Dates(BaseModel):
    staff_id: int
    date_id: str


class Times(BaseModel):
    staff_id: int
    select_date: str
    available_times: list


class SaveTime(BaseModel):
    save_date: str
    save_time: str

class BookingData(BaseModel):
    service_id: int
    staff_id: int
