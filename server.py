#!/usr/bin/python

import logging, signal, random
import tornado.httpserver
import tornado.web
import os, sys, cgi
import base64
from urllib2 import urlparse
from subprocess import Popen
import subprocess
import mutex

logging.basicConfig(level=logging.DEBUG)

sessions = {}
locks = {}

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

class DebugHandler(tornado.web.RequestHandler):
    def get(self, url):
        request = self.request
        filename = 'scripts/' + url + '.input'
        args = request.arguments
        logging.debug('Debugging %s, %s' % (filename, str(args)))
        if not os.path.exists(filename):
            logging.warning('script does not exist!')
            raise tornado.web.HTTPError(404)
        if not sessions.has_key(url):
            script = open(filename, 'r')
            decoded = base64.b64encode(repr(args))
            cmd = 'python trace.py --param="%s"' % decoded
            logging.debug(cmd)
            p = Popen(cmd, shell=True, stdin=script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sessions[url] = p
        src = open(filename, 'r').read()
        self.render('template.html', source=src, random=random.randint(1, 100000), fname=url)

class LogHandler(tornado.web.RequestHandler):
    def get(self, url):
        request = self.request
        if request.path == '/logs':
            try:
                f = open("logs.txt")
                for line in f.readlines():
                    self.write(line)
                    self.write("<br />")
                f.close()
            except:
                self.write('')
                pass

class AjaxHandler(tornado.web.RequestHandler):
    def get(self, url):
        logging.debug('Handling next request %s' % url)
        if not sessions.has_key(url):
            logging.error('Cannot find debug session %s' % url)
            self.write('Not running')
            return
        p = sessions[url]
        # Python 2.5 compatibile way to send signal
        os.kill(p.pid, signal.SIGUSR1)
        # p.send_signal(signal.SIGUSR1)
        count = 0
        terminated = False
        self.write('stdout\n')
        while True:
            line = p.stdout.readline()
            if len(line.strip()) == 0:
                count += 1
                if count > 10:
                    terminated = True
                    break
                continue
            logging.debug(line)
            self.write(line + '\n')
            if line.strip() == 'END':
                break
            if line.strip() == 'TERMINATED':
                terminated = True
                break
        self.write('stderr\n')
        while True:
            line = p.stderr.readline()
            if len(line.strip()) == 0:
                count += 1
                if count > 10:
                    terminated = True
                    break
                continue
            logging.debug(line)
            self.write(line + '\n')
            if line.strip() == 'END':
                break
            if line.strip() == 'TERMINATED':
                terminated = True
                break
        if terminated:
            sessions.pop(url)
            self.write('??')
        
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}


application = tornado.web.Application([
    (r"/(logs)", LogHandler),
    (r"/ajax/(.*)", AjaxHandler),
    (r"/debug/(.*)", DebugHandler),
    (r"/([a-z_0-9]*)", MainHandler),
], **settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(int(sys.argv[1]))
    tornado.ioloop.IOLoop.instance().start()
