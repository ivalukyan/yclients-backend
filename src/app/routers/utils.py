import bcrypt
import asyncio
import re

async def get_times(times: list) -> list:
    """Получение времени"""

    available_times = []

    for time in times:
        available_times.append(time['time'])

    return available_times


async def get_hash(user_id) -> str:
    user_id = user_id.encode('ascii')
    hashed = bcrypt.hashpw(user_id, bcrypt.gensalt())

    return hashed.decode('ascii')


async def get_search(text: str, list_services: dict[str, str], find_field: str) -> list:

    for service in list_services:
        if service[find_field].lower() in text.lower():
            return [service]


async def remove_html_tags(html_content):
    text_only = re.sub(r'<[^>]+>', '', html_content)
    return text_only


async def include_staffs(staff_ids, staff_values) -> list:

    arr = []

    for _ in staff_values:
        if _['staff_id'] in staff_ids:
            arr.append(_)

    return arr