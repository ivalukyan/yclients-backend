import bcrypt
import asyncio

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