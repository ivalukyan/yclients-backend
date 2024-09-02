import os
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
