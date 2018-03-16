#coding: utf-8

import logging

import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer


base = r"musicweb/"

urls = [
    (base+r"index", IndexHandler),
]

application_settings = dict(
    template_path=TEMPLATE_PATH,
    static_path=STATIC_PATH,
    xsrf_cookies=False,
    debug=True
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
