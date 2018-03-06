#coding:utf-8
from sqlalchemy import Column, Integer, ForeignKey

from models.base import ORMBase, engine


class AssociationUserSong(ORMBase):
    user_id = Column(Integer, ForeignKey("user_info._id", name="fk_user_id"))
    song_id = Column(Integer, ForeignKey("songs._id", name="fk_song"))


ORMBase.metadata.create_all(engine)
