#coding:utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from models.base import ORMBase, engine


class Songs(ORMBase):
    _id = Column(Integer, primary_key=True, autoincrement=True)
    uploader = Column(Integer, ForeignKey("user_login._id", name="fk_uploader"))
    name = Column(String(128), nullable=False)
    author = Column(String(128), nullable=False, default="Unkown")
    file_path = Column(String(256), nullable=True)
    description = Column(String(256), nullable=True)
    flag = Column(Integer, nullable=False, default=0)


ORMBase.metadata.create_all(engine)
