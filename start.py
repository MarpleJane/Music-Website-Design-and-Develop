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


BASE = r"musicweb/"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates")
STATIC_PATH = os.path.join(BASE_DIR, "statics")

BACKEND = r"butler/"

urls = [
    (BACKEND+r"login", BackendLogin),
    (BASE+r"index", IndexController),
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
    logging.info("Start application from [%s] port [%s]", __file__, port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
