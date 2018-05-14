#coding: utf-8
"""
  cookie_secret: https://blog.csdn.net/adream307/article/details/7604125
"""

import logging
import os
import base64
import uuid

import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer

from backend import *
from frontend import *

BASE = r"/musicweb/"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates")
STATIC_PATH = os.path.join(BASE_DIR, "statics")

BACKEND = r"/butler/"

urls = [
    (BACKEND+r"login", BackLoginController),
    (BACKEND+r"logout", BackLogoutController),
    (BACKEND+r"welcome", WelcomeController),
    (BACKEND+r"songinfo/([0-9]+)", BackSongInfoController),

    (r"/bpi/songtrail", BackSongTrailController),
    (r"/bpi/songinfo/([0-9]+)", BackSongEditController),
    (r"/bpi/userstatus", BackUserController),

    (BASE+r"index", IndexController),
    (BASE+r"song/([0-9]+)", SongController),
    (BASE+r"space/([0-9]+)", SpaceController),
    (BASE+r"space/contributes/([0-9]+)", ContributeController),
    (BASE+r"space/columns/([0-9]+)", ColumnController),
    (BASE+r"space/column/([0-9]+)", ColumnContentController),
    (BASE+r"space/columns/([0-9]+)/edit", ColumnEditController),
    (BASE+r"space/settings/([0-9]+)", SettingController),
    (BASE+r"signin", FrontSigninController),
    (BASE+r"signup", FrontSignupController),
    (BASE+r"logout", FrontLogoutController),

    (r"/api/userinfochange/([0-9]+)", UserInfoChangeController),
    (r"/api/spiderindex", SpiderIndexController),
    (r"/api/importsong", ImportController),
    (r"/api/allcolumns", ColumnIndexController),
    (r"/api/columnspace/([0-9]+)", ColumnSpaceController),
    (r"/api/songindex/?", SongIndexController),
    (r"/api/songspace", SongSpaceController),
    (r"/api/songtrail", SongTrailController),
    (r"/api/comments?", CommentController),
    (r"/api/carousel", CarouselController),
]

application_settings = dict(
    template_path=TEMPLATE_PATH,
    static_path=STATIC_PATH,
    xsrf_cookies=False,
    debug=True,
    cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
)


def main():
    port = "8888"
    application = tornado.web.Application(
        urls,
        **application_settings
    )
    server = HTTPServer(
        application,
        xheaders=True,
        max_body_size=1024*1024*1024
    )
    server.bind(port)
    server.start(1)
    logging.warn("Start application from [%s] port [%s]", __file__, port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
