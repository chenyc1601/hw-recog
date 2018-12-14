# -*- coding: utf8 -*-

import os.path

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

from neural_network import NeuralNetwork
from img import Image
import pickle
import numpy as np

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
            debug=True
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
        if self.get_argument('actOpt') == 'train' :
            targetDigi = int(self.get_argument('postContent'))
            train(targetDigi)
            self.render(
                "index.html", 
                page_title = "学习一个", 
                header_text = "继续帮助改进吧？" 
            )


class ResultHandler(tornado.web.RequestHandler):
    def post(self) :
        if self.get_argument('actOpt') == 'recog' :
            outputDigi = recognize(self.get_argument('postContent'))
            self.render(
                "result.html", 
                page_title = "数字识别中……", 
                header_text = "认对了吗？", 
                output_content = "图中数字是:{0}".format(outputDigi)
            )


def recognize(imageCode) :
    n = NeuralNetwork(False, 784, 200, 10, 0.01)
    imageArray = Image(imageCode).imgData
    return n.guess(imageArray)


def train(digit) :
    n = NeuralNetwork(False, 784, 200, 10, 0.01)
    with open("imageData.pickle", 'rb') as handle :
        imageArray = pickle.load(handle)
    targetArray = np.zeros(10) + 0.01
    targetArray[int(digit)] = 0.99
    n.train(imageArray, targetArray)
    with open('w_I_H.pickle', 'wb') as handle :
        pickle.dump(n.w_I_H_n, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('w_H_O.pickle', 'wb') as handle :
        pickle.dump(n.w_H_O_n, handle, protocol=pickle.HIGHEST_PROTOCOL)        


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
