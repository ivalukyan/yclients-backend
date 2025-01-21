from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from conf import PostgresConfig


Base = declarative_base()

postgres = PostgresConfig()

db_url = postgres.db_url

engine = create_engine(db_url, pool_pre_ping=True, pool_recycle=300)

# engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)


class BotUser(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False)
    yclients_id = Column(Integer, unique=True, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    fullname = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    is_employee = Column(Boolean, nullable=True)


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)