"""
Schemas app
"""

from pydantic import BaseModel


class Dates(BaseModel):
    content: str


class Times(BaseModel):
    staff_id: int
    date: str