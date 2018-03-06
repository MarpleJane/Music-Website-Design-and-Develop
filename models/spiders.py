#coding:utf-8
from sqlalchemy import Column, ForeignKey, Integer, String
from models.base import ORMBase, engine


class SpiderDsp(ORMBase):
    _id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)


class SpiderRecords(ORMBase):
    _id = Column(Integer, primary_key=True, autoincrement=True)
    dsp_id = Column(Integer, ForeignKey("spider_dsp._id", name="fk_dsp_id"), nullable=False)
    name = Column(String(1024), nullable=True)
    author = Column(String(1024), nullable=True)
    link = Column(String(256), nullable=False)


ORMBase.metadata.create_all(engine)
