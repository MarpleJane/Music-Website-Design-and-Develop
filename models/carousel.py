#coding: utf-8
from sqlalchemy import Column, Integer, String
from models.base import ORMBase, engine


class Carousel(ORMBase):
    """后台上传走马灯图片"""
    _id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(256), nullable=False)
    target = Column(String(256), nullable=False)


ORMBase.metadata.create_all(engine)
