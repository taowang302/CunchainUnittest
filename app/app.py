from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json


# from script import getdb


def get_info(data):
    print('get info')
    return json.dumps({"status": "success"})


def run_case(data):
    print("run case")
    return json.dumps({"status": "success"})


method_dic = {"get_info": get_info, "run_case": run_case}


class TodoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_error(404, "File not found.")
            return
        print(self.path)
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
        msg_return = self.gen_msg(post_values)
        if msg_return[0]:
            self.send_response(200)
        else:
            self.send_response(415)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(msg_return)

    def gen_msg(self, post_body):
        method = post_body.get("method")
        data = post_body.get("data")
        if method_dic.get(method):
            return (True, method_dic.get(method)(data))
        else:
            return (False, json.dumps({"error": "can not understand this method"}))


if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer

    server = HTTPServer(('', 8088), TodoHandler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()
