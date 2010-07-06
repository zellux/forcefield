#!/usr/bin/python

import logging
import tornado.httpserver
import tornado.web
import os, sys
import base64
from urllib2 import urlparse
from subprocess import Popen
import subprocess

logging.basicConfig(level=logging.DEBUG)

class MainHandler(tornado.web.RequestHandler):
    def get(self, url):
        request = self.request
        filename = 'scripts' + request.path + '.input'
        args = request.arguments
        logging.debug(filename + ', ' + str(args))
        if not os.path.exists(filename):
            logging.warning('script does not exist!')
            raise tornado.web.HTTPError(404)
        script = open(filename, 'r')
        decoded = base64.b64encode(repr(args))
        cmd = 'python interpreter.py --nodebug --param="%s"' % decoded
        logging.debug(cmd)
        p = Popen(cmd, shell=True, stdin=script, stdout=subprocess.PIPE)
        output = p.stdout.read()
        self.write(output)
        
application = tornado.web.Application([
    (r"/(.*)", MainHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(int(sys.argv[1]))
    tornado.ioloop.IOLoop.instance().start()
