#coding: utf8
from controller_base import BaseController


class WelcomeController(BaseController):
    """butler/welcome"""
    def get(self):
        self.render("backend/backend.html")
