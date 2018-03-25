#coding: utf8
from tornado.web import RequestHandler
from models import orm_session

class BaseController(RequestHandler):
    def initialize(self):
        self.session = orm_session()

    def current_user(self, end):
        return self.get_secure_cookie("{}".format(end))
