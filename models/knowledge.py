#coding:utf-8
from sqlalchemy import Column, Integer, String

from models.base import ORMBase, engine


class Knowledge(ORMBase):
    _id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    link = Column(String(256), nullable=False)


ORMBase.metadata.create_all(engine)
