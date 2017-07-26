#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import urllib.request
import http.cookiejar
import urllib.parse
import json
#import configparser
import sys
#import MultipartPostHandler

class ConfigHttp:

    def __init__(self, db_cursor,log,archive_id):
        #config = configparser.ConfigParser()
        self.db_cursor = db_cursor.cursor()
        self.log = log
        try:
            self.host,self.port=self.get_config(archive_id)[0][:]
        except:
            raise ValueError('Wrong archive id')
        self.headers = {"Content-Type":"application/json"} 

        #install cookie
        self.cookie = cj = http.cookiejar.CookieJar()
        self.log.debug(cj)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)

    def get_config(self,archive_id):
        self.db_cursor.execute("select host,port from file_bag where file_number='{}'".format(archive_id))
        http_config_list = self.db_cursor.fetchall()[:]
        self.db_cursor.close()
        self.log.info(http_config_list)
        return http_config_list

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return  self.port

    def set_header(self, headers):
        self.headers = headers
    def get(self, url, params,if_get_png=False):
        self.log.debug ("===============\n url => {}\n params => {}\n===================".format(url, params))
        params = urllib.parse.urlencode(eval(params))
        self.log.debug(params)
        self.log.debug(type(params))
        params = params.replace('None','')
        url = "http://{}:{}{}?{}".format(self.host,str(self.port),url,params)
        self.log.info (url)
        request = urllib.request.Request(url, headers=self.headers)
        try:
            response = urllib.request.urlopen(request)
            response_code = response.getcode()
            if if_get_png:
                self.log.info('run in png')
                header = response.headers.get('Content-Type')
                if header == 'image/png':
                    return (response_code,{})
                else:
                    return ("000",{})
            response = response.read().decode('utf-8')
            json_response = json.loads(response)
            self.log.info("receive response:\nresponse_code => {}\nresponse => {}\n========================\n".format(response_code,response))
            return (response_code,json_response)
        except Exception as e:
            self.log.error('%s' % e)
            return ('000',e)
        except:
            return ('000',sys.exc_info()[1])

    def post(self, url, data):
        data = json.dumps(eval(data))
        self.log.debug(data)
        data = data.encode('utf-8')
        url = 'http://' + self.host + ':' + str(self.port)  + url
        self.log.info(url)
        self.log.debug("send message:\n".format(data))
        try:
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request, data)
            response_code = response.getcode()
            response = response.read().decode('utf-8')
            json_response = json.loads(response)
            self.log.info("receive response:\nresponse_code => {}\nresponse => {}\n========================\n".format(response_code,response))
            return (response_code,json_response)
        except Exception as e:
            self.log.error('%s' % e)
            return ('000',e)
        except:
            return ('000',sys.exc_info()[1]) 

    def post_file(self,url,file_path):
        with open(file_path,"rb") as f:
            post_data = f.read()
        files = {"form_input_field_name": post_data}
        payload = {"name":"resaon","reason":"id_card_image_0"}
        url = 'http://' + self.host + ':' + str(self.port)  + url
        try:
            self.log.debug(url)
            ret = requests.post(url, files=files,data=payload,cookies=self.cookie)
        except:
            self.log.error("Upload img failed\n{}".format(sys.exc_info()))
            return ('000',sys.exc_info()[1])
        else:
            return (ret.status_code,ret.text)
