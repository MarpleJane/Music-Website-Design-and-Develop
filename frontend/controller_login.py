#coding: utf8
import logging

from models import UserLogin, UserInfo
from controller_base import BaseController


class FrontSigninController(BaseController):
    """musicweb/signin
       登录
    """
    def post(self):
        user = self.get_argument("user")
        password = self.get_argument("password")

        ur = self.session.query(UserLogin).\
                filter(UserLogin.account==user).\
                first()
        flag = False
        if ur:
            if ur.status == 0:
                if ur.password == password:
                    flag = True
                if not flag:
                    self.write(dict(ret=1, msg="Password error"))
                else:
                    self.set_secure_cookie("user_id", str(ur._id), expires_days=None)
                    self.write(dict(ret=0, msg="Login success", url="index"))
            else:
                self.write(dict(ret=1, msg="用户被禁用"))
        else:
            self.write(dict(ret=1, msg="User not exist"))


class FrontSignupController(BaseController):
    """musicweb/signup
       注册
    """
    def post(self):
        user = self.get_argument("user")
        password = self.get_argument("password")

        ur = self.session.query(UserLogin).\
                filter(UserLogin.account==user).\
                first()
        flag = False
        if ur:
            self.write(dict(ret=1, msg="Username has been used"))
        else:
            new_user = UserLogin(account=user, password=password)
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            new_info = UserInfo(login_id=new_user._id)
            self.session.add(new_info)
            self.session.commit()
            self.set_secure_cookie("user_id", str(new_user._id), expires_days=None)
            self.write(dict(ret=0, msg="吾即汝，汝即吾，即刻起，契约签订", url="index"))


class FrontLogoutController(BaseController):
    """musicweb/logout"""
    def get(self):
        if self.current_user("user_id"):
            self.clear_cookie("user_id")
        self.redirect("index")
