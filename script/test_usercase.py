import json
import sys
try:
    from urllib2 import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener, install_opener, urlopen, Request, HTTPError
except ImportError:
    from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener, install_opener, urlopen, Request


class TestCase():
    # def __init__(self,host,port,timeout=3):
    #     self.host = host
    #     self.port = port
    #     self.time_out = timeout

    def test_case_cmd(base_url,queryparameters,command, *args):
        request = {
                   'jsonrpc' :'2.0',
                   'id' : 0,
                   'method' : command
        }
        #print args
        #print len(args)
        if len(args) == 1 and None not in args:
            request['params']=args[0]
        elif len(args) > 1:
            return json.loads({'code':1,'status':'fail','information':'length of command bigger then 1'})
        url = 'http://{}{}'.format(base_url,queryparameters)
        #print url
        #print json.dumps(request).encode('utf-8')
        passman=HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url,None,None)
        auth_handler=HTTPBasicAuthHandler(passman)
        opener=build_opener(auth_handler)
        install_opener(opener)
        #Request.add_header('Content-Type','application/json')
        try:
            raw_request = Request(url=url, data=json.dumps(request).encode('utf-8'))
            raw_request.add_header('Content-Type','application/json')
            #raw_result=urlopen(url, json.dumps(request).encode('utf-8'), self.time_out,headers).read()
            raw_result=urlopen(raw_request).read()
        except HTTPError,e:
            # print e.code
            return_detail = e.read()
            result_array=json.loads(return_detail)
            print result_array
            return json.dumps({"code":1,"status":"fail","information":result_array.get("error")})
        except:
            print sys.exc_info()
        else:
            result_array=json.loads(raw_result.decode('utf-8'))
            print result_array
            return json.dumps({"code":0,"status":"success","information":result_array['result']})
        #print result
        #return
