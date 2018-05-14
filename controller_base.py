#coding: utf8
import json

from tornado.web import RequestHandler
from models import orm_session
from models import UserLogin, UserInfo, Songs
from tools import cached_property


class BaseController(RequestHandler):
    def initialize(self):
        # self.session = orm_session()
        pass

    @cached_property
    def session(self):
        return orm_session()

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def current_user(self, end):
        return self.get_secure_cookie("{}".format(end))

    def user_login(self):
        user_info = {"user_id": 0, "username": "", "avatar": ""}
        user_id = self.current_user("user_id")
        if user_id:
            ur = self.session.query(UserLogin).\
                    filter(UserLogin._id==user_id).\
                    first()
            uin = self.session.query(UserInfo).\
                    filter(UserInfo.login_id==user_id).\
                    first()
            user_info["user_id"] = ur._id
            user_info["username"] = ur.account
            user_info["avatar"] = uin.avatar
            user_info["status"] = ur.status
        return user_info

    def user_info(self, user_id):
        ur = self.session.query(UserLogin).\
                filter(UserLogin._id==user_id).\
                first()
        return dict(
            user_id = ur._id,
            username = ur.account,
            desc = ur.info[0].description,
            avatar = ur.info[0].avatar,
            status = ur.info[0].status
        )

    def trail_pass(self):
        return self.session.query(Songs).filter(Songs.flag==1)

    def trail_unpass(self):
        return self.session.query(Songs).filter(Songs.flag==2)

