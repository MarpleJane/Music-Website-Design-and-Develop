#coding:utf-8
from sqlalchemy import Column, Integer, ForeignKey

from models.base import engine, ORMBase


class AssociationUserSong(ORMBase):
    _id = Column(Integer, primary_key=True, autoincrement=True)
    amateur = Column(Integer, ForeignKey("user_info.login_id", name="fk_amateur"), nullable=False)
    favor = Column(Integer, ForeignKey("songs._id", name="fk_favor"), nullable=False)


ORMBase.metadata.create_all(engine)
