async def get_times(times: list) -> list:
    """Получение времени"""

    available_times = []

    for time in times:
        available_times.append(time['time'])

    return available_times