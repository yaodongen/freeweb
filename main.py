#! /usr/bin/python
# -*- coding:utf8 -*-
import tornado.ioloop
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from web.home import BaseHandler,MainHandler,DonateHandler,LoginHandler,UserHandler

define("port", default=9000, help="run on the given port", type=int)
from settings import settings

app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/donate", DonateHandler),
    (r"/user", UserHandler),
], **settings)

"""
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
"""




if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
