#coding: utf8
import logging

from controller_base import BaseController
from models import Songs, UserLogin
from tools import get_obj_attrs, get_attrs


class WelcomeController(BaseController):
    """butler/welcome"""
    def get(self):
        self.render("backend/backend.html")


class BackSongInfoController(BaseController):
    """butler/songinfo/([0-9]+)"""
    def get(self, song_id):
        song_id = int(song_id)
        song = self.session.query(Songs).\
            filter(Songs._id==song_id).\
            first()
        self.render("backend/song.html", song_id=song_id, name=song.name, author=song.author, file_path=song.file_path, cover_path=song.cover_path)


class BackSongTrailController(BaseController):
    """/bpi/songtrail"""
    attrs = ["name", "flag", "burl", "_id"]
    def get(self):
        songs = self.session.query(Songs).all()
        song_list = get_attrs(self.attrs, songs)
        self.write(dict(song_list=song_list))


class BackSongEditController(BaseController):
    """/bpi/songinfo/([0-9]+)"""
    attrs = ["name", "file_path", "description", "origin_type", "cover_path", "author", "flag", "_id"]
    def get(self, song_id):
        song_id = int(song_id)
        song = self.session.query(Songs).\
            filter(Songs._id==song_id).\
            first()
        song_type = song.type_info.type_name
        song_info = get_obj_attrs(self.attrs, song)
        song_info["type_name"] = song_type
        self.write(dict(song_info=song_info))

    def post(self, song_id):
        new_flag = self.get_argument("flag")
        new_flag = int(new_flag)
        song = self.session.query(Songs).\
            filter(Songs._id==song_id).\
            first()
        song.flag = new_flag
        self.session.commit()
        self.write(dict(ret=0))


class BackUserController(BaseController):
    """/bpi/userstatus"""
    attrs = ["_id", "account", "status"]
    def post(self):
        user_id = self.get_argument("user_id")
        user_id = int(user_id)
        status = self.get_argument("status")
        user = self.session.query(UserLogin).\
            filter(UserLogin._id==user_id).\
            first()
        user.status = int(status)
        self.session.commit()
        self.write(dict(ret=0))

    def get(self):
        users = self.session.query(UserLogin).all()
        user_list = get_attrs(self.attrs, users)
        self.write(dict(user_list=user_list))
