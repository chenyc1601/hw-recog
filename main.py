# -*- coding: utf8 -*-

import os.path

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

from neural_network import NeuralNetwork
from img import Image

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html", 
            page_title = "Title", 
            header_text = "Index", 
            output_content = ""
        )

    def post(self) :
        outputDigi = self.recognize(self.get_argument('imageCode'))
        self.render(
            "index.html", 
            page_title = "Title", 
            header_text = "Index", 
            ## output_content = self.get_argument('imageCode')
            output_content = "图中数字是:{0}".format(outputDigi)
        )

    def recognize(self, imageCode) :
        n = NeuralNetwork(False, 784, 200, 10, 0.01)
        imageArray = Image(imageCode).imgData
        return n.guess(imageArray)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
