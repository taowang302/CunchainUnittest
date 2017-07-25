from http.server import BaseHTTPRequestHandler
import cgi
import json
import  urllib.parse
import sys

from control_center import Control

def get_info(data):
    return_msg = Control().get_info()
    print('get info\n{}'.format(return_msg))
    return return_msg 


def run_case(data):
    Control.run_case()
    print("run case")
    return json.dumps({"status": "success"})


method_dic = {"get_info": get_info, "run_case": run_case}


class TodoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_error(404, "File not found.")
            return
        parse_path = urllib.parse.urlparse(self.path)
        query_dic = urllib.parse.parse_qs(parse_path.query, True)
        print(query_dic)
        msg_return = self.gen_msg(query_dic)
        print (msg_return)
        if msg_return[0]:
            self.send_response(msg_return[1])
        else:
            self.send_response(msg_return[1])
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(eval(msg_return[2])))

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        print("ctype:{},type:{}\npdict:{},type:{}".format(ctype,type(ctype),pdict,type(pdict)))
        if ctype == 'application/json':
            length = int(self.headers['content-length'])
            print(length)
            post_values = self.rfile.read(length).decode()
            post_values = json.loads(post_values)
            print(post_values)
        else:
            self.send_error(415, "Only json data is supported.")
            return
        msg_return = self.gen_msg(post_values)
        if msg_return[0]:
            self.send_response(msg_return[1])
        else:
            self.send_response(msg_return[1])
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        print(msg_return[2])
        print(type(msg_return[2]))
        self.wfile.write(json.dumps(msg_return[2]).encode(encoding="utf-8"))

    def gen_msg(self, post_body):
        method = ''.join((post_body.get("method")))
        print (method)
        data = post_body.get("data")
        if method_dic.get(method):
            try:
                return_data = method_dic.get(method)(data)
            except:
                return (True, 500, sys.exc_info()[1])
            else:
                return (True, 200, return_data)
        else:
            return (False, 400, json.dumps({"error": "can not understand this method"}))


if __name__ == '__main__':
    from http.server import HTTPServer

    # control=control_center.Control()
    server = HTTPServer(('', 8088), TodoHandler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()
