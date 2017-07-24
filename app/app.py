from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
from script import getdb


def get_info():
    pass


method_dic = {}


class TodoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_error(404, "File not found.")
            return
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(self.gen_msg('get_name'))

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'application/json':
            length = int(self.headers['content-length'])
            post_values = json.loads(self.rfile.read(length))
        else:
            self.send_error(415, "Only json data is supported.")
            return
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(self.gen_msg(post_values))

    def gen_msg(self, post_body):
        method = post_body.get("method")
        information = post_body.get("information")
        return method_dic.get(method)(information)


if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer

    server = HTTPServer(('', 8888), TodoHandler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()
