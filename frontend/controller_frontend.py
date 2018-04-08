#coding: utf8
from controller_base import BaseController


class IndexController(BaseController):
    "musicweb"
    def get(self):
        self.render("frontend/frontpage.html")


class SongController(BaseController):
    "song/([0-9]+)"
    def get(self):  # TODO
        self.render("frontend/songpage.html")


class SpaceController(BaseController):
    "space/([0-9]+)"
    def get(self):
        self.render("frontend/userpage.html")
