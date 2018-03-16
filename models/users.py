#coding:utf-8
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from models.base import ORMBase, engine


class UserLogin(ORMBase):
    """用户登录信息"""
    _id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(64), nullable=False)
    password = Column(String(128), nullable=False)
    info = relationship("UserInfo")
    upload_songs = relationship("Songs")


class UserInfo(ORMBase):
    """用户具体信息"""
    _id = Column(Integer, primary_key=True, autoincrement=True)
    login_id = Column(Integer, ForeignKey("user_login._id", name="fk_login"))
    description = Column(String(128), nullable=False, default="这个人很懒，什么都没有留下")
    created_datetime = Column(DateTime, default=datetime.datetime.now)


ORMBase.metadata.create_all(engine)
