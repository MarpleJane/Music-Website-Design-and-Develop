#coding:utf-8
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from models.base import ORMBase, engine
from models.users import UserLogin, UserInfo


class SongType(ORMBase):
    """歌曲类型, 0代表其他"""
    _id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(32))


class Songs(ORMBase):
    """上传的和收藏的歌曲"""
    _id = Column(Integer, primary_key=True, autoincrement=True)
    uploader = Column(Integer, ForeignKey("user_login._id", name="fk_uploader"))
    name = Column(String(128), nullable=False)
    cover_path = Column(String(256), nullable=True)
    author = Column(String(128), nullable=False, default="Unkown")
    file_path = Column(String(256), nullable=True)
    description = Column(String(256), nullable=True)
    flag = Column(Integer, nullable=False, default=0)  # 审核
    origin = Column(Integer, nullable=False, default=1)  # 原创：1；非原创：2
    type_id = Column(Integer, ForeignKey("song_type._id", name="fk_type"), nullable=False, default=0)  # 歌曲类型
    play_times = Column(Integer, nullable=False, default=0)  # 播放次数/点击量
    rate = Column(Float, nullable=False, default=0)  # 打分
    created_time = Column(DateTime, default=datetime.datetime.now)
    
    comments = relationship("Comments")
    type_info = relationship("SongType")
    uploader_info = relationship("UserLogin")

    @property
    def url(self):
        return "/musicweb/song/" + str(self._id)

    @property
    def song_type(self):
        return self.type_info.type_name

    @property
    def uploader_name(self):
        uploader = self.uploader_info.account
        return uploader

    @property
    def origin_type(self):
        origin_dict = {1: "原创", 2: "非原创"}
        return origin_dict[self.origin]

    @property
    def flag_name(self):
        flag_dict = {0: "未审核", 1: "通过", 2: "未通过"}
        return flag_dict[self.flag]

    @property
    def burl(self):
        return "/butler/songinfo/" + str(self._id)


class Comments(ORMBase):
    """歌曲评论"""
    _id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(256))
    author_id = Column(Integer, ForeignKey("user_login._id", name="fk_comment_author"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs._id", name="fk_comment_song"), nullable=False)
    created_time = Column(DateTime, default=datetime.datetime.now)

    author = relationship("UserLogin")

    @property
    def username(self):
        return self.author.account

    @property
    def avatar(self):
        return self.author.avatar


ORMBase.metadata.create_all(engine)
