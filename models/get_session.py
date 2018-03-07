#coding: utf-8
from sqlalchemy.orm import sessionmaker

from models.base import engine


def orm_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
