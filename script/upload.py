#!/usr/bin/python2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import sys
import json
class UploadFile():
    def __init__(self):
        self.dst_host = ''
        self.file_path = ''
        self.cookie = ''

    def set_upload(self,dst_host):
        self.dst_host = dst_host

    def add_file(self,file_name):
        self.file_path = file_name

    def add_cookie(self,cookie):
        self.cookie = cookie

    def upload(self):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)
        register_openers()
        try:
            with open(self.file_path,"rb") as f:
                file_data = f.read()
                datagen, headers = multipart_encode({"image1": file_data})
                request = urllib2.Request(self.dst_host, datagen, headers)
                return urllib2.urlopen(request).read()
        except:
                return json.dumps({"status":"fail","reason":'{}'.format(sys.exc_info()[1])})

    def parese_file(self):
        register_openers()
        try:
            with open(self.file_path,"rb") as f:
                file_data = f.read()
                datagen, headers = multipart_encode({"image1": file_data})
                return {"datagen":datagen,"headers":headers}
        except:
            return json.dumps({"status":"fail","reason":'{}'.format(sys.exc_info()[1])})

if "__main__" == __name__:
    upload = UploadFile()
    upload.set_upload("http://116.62.173.114:8888/api/v0/upload/img")
    upload.add_file("/tmp/1.png")
    upload.add_cookie('')
    #print upload.upload()
    print (upload.parese_file())
