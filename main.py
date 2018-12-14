# -*- coding: utf8 -*-

import os.path

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

from neural_network import NeuralNetwork
from img import Image
import pickle

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/handwriting", IndexHandler), 
            (r"/handwriting/result", ResultHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Train": TrainModule}, 
            debug=False
            )
        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html", 
            page_title = "手写数字识别", 
            header_text = "欢迎~"
        )

    def post(self):
        #TODO: 训练之后重新加载首页
        pass


class ResultHandler(tornado.web.RequestHandler):
    def post(self) :
        if self.get_argument('actOpt') is 'recog' :
            outputDigi = self.recognize(self.get_argument('postContent'))
            self.render(
                "index.html", 
                page_title = "数字识别中……", 
                header_text = "认对了吗？", 
                ## output_content = self.get_argument('imageCode')
                output_content = "图中数字是:{0}".format(outputDigi), 
            )

        elif self.get_argument('actOpt') is 'train' :
            targetDigi = int(self.get_argument('postContent'))
            self.render(
                "index.html", 
                page_title = "学习一个", 
                header_text = "帮助改进", 
                ## output_content = self.get_argument('imageCode')
                output_content = "图中数字是:{0}".format(outputDigi), 
            )


    def recognize(self, imageCode) :
        n = NeuralNetwork(False, 784, 200, 10, 0.01)
        imageArray = Image(imageCode).imgData
        return n.guess(imageArray)

    def train(self, digit) :
        #TODO: 训练
        n = NeuralNetwork(False, 784, 200, 10, 0.01)
        with open("imageData.pickle", 'rb') as handle :
            imageArray = pickle.load(handle)
        n.train()


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
