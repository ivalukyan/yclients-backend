"""
Schemas app
"""

from pydantic import BaseModel


class SaveDate(BaseModel):
    content: str