import httpx


class YclientRecords:
    def __init__(self, fullname, phone, email, appointments, comment):
        # Имя клиента
        self.fullname = fullname

        # Телефон клиента (пример 79161502239)
        self.phone = phone

        # Почтовый адрес клиента
        self.email = email

        # Параметры услуги
        self.appointments = appointments

        # Комментарий к записи
        self.comment = comment

    def adding_record(self):
        pass
