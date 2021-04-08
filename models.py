from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import Date
from database import Base
import datetime


class Ips(Base):
    __tablename__ = "Ips"

    id = Column(Integer, primary_key=True)
    ip = Column(String)
    time = Column(DateTime)
    email = Column(String)


class Worker(Base):
    __tablename__ = "Worker"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    time = Column(DateTime, default=datetime.datetime.now().strftime("%H:%M:%S.%f"))
    n = Column(String)
    p = Column(String)
    q = Column(String)
    status = Column(String)
    time_started = Column(String)
    time_ended = Column(String)


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    code = Column(String)
    status = Column(String)
