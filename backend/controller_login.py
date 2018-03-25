#! coding: utf8
import logging

from models import AdminInfo
from controller_base import BaseController

class BackLoginController(BaseController):
    """butler/login"""
    def get(self):
        if self.current_user("admin_id"):
            self.redirect("welcome")
            return
        self.render("backend/login.html")

    def post(self):
        admin = self.get_argument("admin")
        password = self.get_argument("password")

        ad = self.session.query(AdminInfo).\
                filter(AdminInfo.account==admin).\
                first()
        flag = False
        if ad:
            if ad.password == password:
                flag = True
            if not flag:
                self.write(dict(ret=1, msg="Password error"))
            else:
                self.set_secure_cookie("admin_id", str(ad._id), expires_days=None)
                #self.redirect("welcome")
                self.write(dict(ret=0, msg="Login success", url="welcome"))
        else:
            self.write(dict(ret=1, msg="Admin not exist"))


class BackLogoutController(BaseController):
    """butler/logout"""
    def get(self):
        if self.current_user("admin_id"):
            self.clear_cookie("admin_id")  # the effect will not be seen until the following request

        self.redirect("login")
