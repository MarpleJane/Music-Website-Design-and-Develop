#! coding: utf8
from models import AdminInfo
from controller_base import BaseController

class LoginController(BaseController):
    """butler/login"""
    def get(self):
        if self.current_user("admin_id"):
            self.redirect("") #TODO redirect to manage uri
            return
        self.render("backend/login.html")

    def post(self):
        admin = self.get_argument("admin")
        password = self.get_argument("password")

        ad = self.session.query(AdminInfo).\
                filter(AdminInfo.account==admin).\
                first()
        if not ad:
            self.write()  # TODO return account not exist

        if ad.password != password:
            self.write()  # TODO return password error

        self.set_secure_cookie("admin_id", ad._id, expires_days=None)

        self.redirect("")  # TODO redirect to manage uri


class LogoutController(BaseController):
    """butler/logout"""
    def get(self):
        if self.current_user("admin_id"):
            self.clear_cookie("admin_id")  # the effect will not be seen until the following request

        self.redirect("butler/login")
