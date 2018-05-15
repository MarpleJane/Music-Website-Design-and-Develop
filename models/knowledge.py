#coding:utf-8
import logging
import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from models.base import ORMBase, engine
from models.users import UserInfo, UserLogin


class Knowledge(ORMBase):
    """科普"""
    _id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    link = Column(String(256), nullable=False)


class Columns(ORMBase):
    """专栏"""
    _id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    author_id = Column(Integer, ForeignKey("user_login._id", name="fk_column"), nullable=False)
    click_times = Column(Integer, nullable=False, default=0)
    store_url = Column(String(256), nullable=False)
    created_time = Column(DateTime, default=datetime.datetime.now)

    user = relationship("UserLogin", backref="comments")

    def get_author_name(self):
        return self.user.account

    @property
    def author(self):
        return self.get_author_name()

    @property
    def url(self):
        return "/musicweb/space/column/" + str(self._id)

ORMBase.metadata.create_all(engine)
