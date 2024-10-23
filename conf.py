import os
from dotenv import load_dotenv

from dataclasses import dataclass

load_dotenv()


@dataclass
class YclientsConfig:
    """ENV variables"""
    def __init__(self) -> None:
        self.bearer = os.getenv("BEARER_TOKEN")
        self.user = os.getenv("USER_TOKEN")
        self.company_id = os.getenv("COMPANY_ID")
        self.login = os.getenv("YCLIENT_LOGIN")
        self.password = os.getenv("YCLIENT_PASSWORD")


@dataclass
class PostgresConfig:
    def __init__(self) -> None:
        self.db_url = os.getenv("DB_URL")