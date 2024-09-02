import httpx
import ujson
import logging
import asyncio
import os
import uuid

from uuid import uuid4
from dotenv import load_dotenv


load_dotenv()


class YclientsConfig:
    """ENV variables"""
    def __init__(self) -> None:
        self.bearer = os.getenv("BEARER_TOKEN")
        self.user = os.getenv("USER_TOKEN")
        self.company_id = os.getenv("COMPANY_ID")
        self.login = os.getenv("YCLIENT_LOGIN")
        self.password = os.getenv("YCLIENT_PASSWORD")


yclient = YclientsConfig()


class Yclient:
    def __init__(self, bearer_token: str, company_id: int, user_token: str = "", language: str = "ru-RU") -> None:
        self.company_id = company_id
        self.headers = {
            "Accept": "application/vnd.yclients.v2+json",
            "Accept-Language": language,
            "Authorization": f"Bearer {bearer_token}, User {user_token}",
            "Cache-Control": "no-cache"
        }
        self.logging = False


        @staticmethod
        def logging():
            logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


    async def user_token(self, login: str, password: str) -> None:
        url = f"https://api.yclients.com/api/v1/auth"
        payload = {
            "login": login,
            "password": password
        }
        async with httpx.AsyncClient() as c:
            response = await c.post(url=url, json=payload, headers=self.headers)
        res = ujson.loads(response.text)

        if res['success']:
            return res['data']['user_token']
        else:
            print("Ошибка запроса")



    async def book_services(self) -> None:
        url = f"https://api.yclients.com/api/v1/book_services/{self.company_id}"

        async with httpx.AsyncClient() as c:
            response = await c.get(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        services = {}

        if res['success']:
            data = res['data']
            if not data['services']:
                return "Услуги для бронирования отсутствуют"
            else:
                service = data['services']
                for _ in range(len(service)):
                    services[uuid4().hex] = {'service_id': service[_]['id'], 'service_title': service[_]['title']}

                return services
            
        return "Ошибка запроса"
    

    async def book_dates(self) -> None:
        url = f"https://api.yclients.com/api/v1/book_dates/{self.company_id}"
        async with httpx.AsyncClient() as c:
            response = await c.get(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        booking_dates = {}

        if res['success']:
            data = res['data']
            for _ in range(len(data['booking_dates'])):
                booking_dates[uuid4().hex] = {'book_date': data['booking_dates'][_]}

            return booking_dates
        return "Ошибка запроса"
    

    async def book_staff(self) -> None:
        url = f"https://api.yclients.com/api/v1/book_staff/{self.company_id}"
        async with httpx.AsyncClient() as c:
            response = await c.get(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        staff = {}

        if res['success']:
            data = res['data']
            for _ in range(len(data)):
                staff[uuid4().hex] = {"staff_id": data[_]['id'], "staff_name": data[_]['name'], "staff_specialization": data[_]['specialization'],
                                      "staff_avatar": data[_]['avatar'], "staff_info": data[_]['information']}
                
            return staff
        return "Ошибка запроса"
    

    async def book_times(self, staff_id: dict, date: str) -> None:

        times = {}

        url = f"https://api.yclients.com/api/v1/book_times/{self.company_id}/{staff_id}/{date}"

        async with httpx.AsyncClient() as c:
            response = await c.get(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if res['success']:

            for _ in res['data']:
                times[uuid4().hex] = {'date': date, 'time': _['time']}


            return times


    async def create_booking(self, phone: str, fullname: str, email: str, comment: str, service_id: int,
                              staff_id: int, date_id:str, time_id:str):
        url = f"https://api.yclients.com/api/v1/book_record/{self.company_id}"
        payload = {
            "phone": phone[-11:],
            "fullname": fullname,
            "email": email,
            "comment": comment,
            "appointments": [
                {
                    "id": 1,
                    "services": [
                        service_id
                    ],
                    "staff_id": staff_id,
                    "datetime": f'{date_id}T{time_id}',
                }
            ]
        }
        async with httpx.AsyncClient() as c:
            response = await c.post(url=url, json=payload, headers=self.headers)
        res = ujson.loads(response.text)

        return res


async def main():
    api = Yclient(bearer_token=yclient.bearer, company_id=yclient.company_id, user_token=yclient.user)

    # print("user token - %s" % (await api.user_token(login=yclient.login, password=yclient.password)))
    # print(await api.book_services())
    # print(await api.book_dates())
    # print(await api.book_staff())
    # staff = await api.book_staff()
    # dates = await api.book_dates()

    # print(await api.book_times(staff=staff, dates=dates))


if __name__ == '__main__':
    asyncio.run(main())
