#coding:utf-8
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from models.base import ORMBase, engine


class SpiderDsp(ORMBase):
    """爬虫渠道"""
    _id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    link = Column(String(256), nullable=False)


class SpiderRecords(ORMBase):
    """存放爬到的歌曲链接"""
    _id = Column(Integer, primary_key=True, autoincrement=True)
    dsp_id = Column(Integer, ForeignKey("spider_dsp._id", name="fk_dsp_id"), nullable=False)
    name = Column(String(1024), nullable=True)
    author = Column(String(1024), nullable=True)
    link = Column(String(256), nullable=False)
    created_datetime = Column(DateTime, nullable=False, default=datetime.datetime.now)


ORMBase.metadata.create_all(engine)
