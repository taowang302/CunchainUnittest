from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import cgi
import json
from socketserver import ThreadingMixIn
import urllib.parse
import sys
# from control_center import GlobalConfig
from control_center import Control
import re

import os
import signal
import subprocess


class Daemon(object):
    def __init__(self, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=int('022'), verbose=1):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.home_dir = home_dir
        self.verbose = verbose
        self.umask = umask
        self.daemon_alive = True

    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        os.chdir(self.home_dir)
        os.setsid()
        os.umask(self.umask)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(
                "fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        if sys.platform != 'darwin':
            sys.stdout.flush()
            sys.stderr.flush()
            si = open(self.stdin, 'r')
            so = open(self.stdout, 'ab')
            if self.stderr:
                se = open(self.stderr, 'ab', 0)
            else:
                se = so
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

        def sigtermhandler(signum, frame):
            self.daemon_alive = False
            signal.signal(signal.SIGTERM, sigtermhandler)
            signal.signal(signal.SIGINT, sigtermhandler)

        if self.verbose >= 1:
            print("Server Started")
        pid = str(os.getpid())

    def start(self, command_list):
        if self.verbose >= 1:
            print("Starting Server...")
        self.daemonize()
        self.run(command_list)

    def is_running(self):
        pid = self.get_pid()
        print(pid)
        return pid and os.path.exists('/proc/%d' % pid)

    def run(self, command_list):
        command_list()
        # subprocess.Popen(command_list)

def get_info(data):
    return_msg = control.get_info()
    return return_msg 


def run_case(data):
    return_msg = control.run_case(data)
    return return_msg

def get_case_info(data):
    return_msg = control.get_case_info(data)
    return return_msg


# 接口函数字典表
method_dic = {"get_info": get_info, "run_case": run_case, "get_case_info":get_case_info}


class TodoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        log.info('receive request GET {}'.format(self.path))
        if self.path == '/':
            log.error('error request')
            self.send_error(404, "File not found.")
            return
        elif re.match('^/report(.*?)html$', self.path):
            html_path = '../html/{}'.format(self.path.split('/')[1])
            log.info(html_path)
            try:
                with open(html_path, 'rb') as f:
                    self.send_response(200)
                    response_mesg = f.read()
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', len(response_mesg))
                    self.end_headers()
                    self.wfile.write(response_mesg)
                    return
            except:
                log.error(sys.exc_info())
                self.send_error(404, "File not found.")
                return
        elif self.path == '/favicon.ico':
            try:
                with open('../html/favicon.png', 'rb') as f:
                    log.info('response 200')
                    self.send_response(200)
                    response_mesg = f.read()
                    self.send_header('Content-type', 'image/x-icon')
                    self.send_header('Content-Length', len(response_mesg))
                    self.end_headers()
                    self.wfile.write(response_mesg)
                    return
            except:
                log.error('response 404 {}'.format(sys.exc_info()))
                self.send_error(404, "File not found.")
                return
        parse_path = urllib.parse.urlparse(self.path)
        query_dic = urllib.parse.parse_qs(parse_path.query, True)
        msg_return = self.gen_msg(query_dic)
        self.send_response(msg_return[1])
        log.info('send response {}'.format(msg_return[1]))
        response_mesg = json.dumps(msg_return[2]).encode(encoding="utf-8")
        log.debug('send response:\n{}'.format(json.dumps(msg_return[2], indent=4, sort_keys=False, ensure_ascii=False)))
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', len(response_mesg))
        self.end_headers()
        self.wfile.write(response_mesg)

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        # print("ctype:{},type:{}\npdict:{},type:{}".format(ctype,type(ctype),pdict,type(pdict)))
        if ctype == 'application/json':
            length = int(self.headers['content-length'])
            post_values = self.rfile.read(length).decode()
            post_values = json.loads(post_values)
            log.info(post_values)
        else:
            log.error("not json data which received")
            self.send_error(415, "Only json data is supported.")
            return
        msg_return = self.gen_msg(post_values)
        self.send_response(msg_return[1])
        log.info('response {}'.format(msg_return[1]))
        response_mesg = json.dumps(msg_return[2]).encode(encoding="utf-8")
        log.debug('send response:\n{}'.format(json.dumps(msg_return[2], indent=4, sort_keys=False, ensure_ascii=False)))
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', len(response_mesg))
        self.end_headers()
        self.wfile.write(response_mesg)

    def gen_msg(self, post_body):
        try:
            method = ''.join((post_body.get("method")))
            log.debug('method is {}'.format(method))
            data = post_body.get("data")
            log.debug('data is {}'.format(data))
        except:
            log.error(sys.exc_info())
            # print(sys.exc_info())
            return (False, 400, json.dumps({"error": "can not understand this method"}))
        if method_dic.get(method):
            try:
                return_data = method_dic.get(method)(data)
            except:
                return (True, 500, sys.exc_info()[1])
            else:
                if return_data.get('status') == 'success':
                    return (True, 200, return_data)
                else:
                    return(True,500,return_data)
        else:
            log.error('can not understand this method')
            return (False, 400, json.dumps({"error": "can not understand this method"}))

class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':
    control = Control()
    # global_config = GlobalConfig()
    log = control.log
    host, port = control.get_server_config()
    try:
        # Single thread
        server = HTTPServer((host, port), TodoHandler)

        # Multithreading
        # server = ThreadingServer((host, port), TodoHandler)
    except OSError as e:
        print('OSError: [Errno {}] {}'.format(e.errno, e.strerror))
        sys.exit()
    if host:
        listen_host = host
    else:
        listen_host = '0.0.0.0'
    log.info("Starting server on {}:{}".format(listen_host, port))

    if len(sys.argv) == 1:
        try:
            print("Starting server on {}:{}, use <Ctrl-C> to stop".format(listen_host, port))
            server.serve_forever()
        except KeyboardInterrupt:
            log.info('quit with <Ctrl-C>')
            print('<Ctrl-C>')
        except:
            log.error('quit with error:{}'.format(sys.exc_info()))
            print('unknown error')

    else:
        if sys.argv[1] == '-d':
            log.debug(sys.argv)
            demo = Daemon()
            demo.start(server.serve_forever)
