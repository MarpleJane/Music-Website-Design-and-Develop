#coding: utf8
import json

from tornado.web import RequestHandler
from models import orm_session
from models import UserLogin, UserInfo


class BaseController(RequestHandler):
    def initialize(self):
        self.session = orm_session()

    def current_user(self, end):
        return self.get_secure_cookie("{}".format(end))

    def user_login(self):
        user_info = {"user_id": 0, "username": "test"}
        user_id = self.current_user("user_id")
        if user_id:
            ur = self.session.query(UserLogin).\
                    filter(UserLogin._id==user_id).\
                    first()
            user_info["user_id"] = ur._id
            user_info["username"] = ur.account
        return user_info

    def user_info(self, user_id):
        ur = self.session.query(UserLogin).\
                filter(UserLogin._id==user_id).\
                first()
        return dict(
            user_id = ur._id,
            username = ur.account,
            desc = ur.info[0].description,
            avatar = ur.info[0].avatar
        )

