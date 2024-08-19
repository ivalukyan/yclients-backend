import os
from dotenv import load_dotenv

load_dotenv()


class Postgres:
    def __init__(self):
        self.db = os.getenv('POSTGRES_DB')
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.port = os.getenv('POSTGRES_PORT')
        self.host = os.getenv('POSTGRES_HOST')


class YclientsENV:
    def __init__(self):
        self.company_id = os.getenv('CID')
