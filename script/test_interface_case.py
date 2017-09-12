#!/usr/bin/env python
# -*- coding:utf-8 -*-


import unittest
import json
import os
import sys
import string
from random import randint, choice

class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """

    def __init__(self, methodName='runTest', test_data=None, http=None, db_cursor=None, db2_cursor=None, log=None,
                 archive_id=None, view_id=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.test_data = test_data
        self.http = http
        self.db_cursor = db_cursor
        self.db2_cursor = db2_cursor
        self.log = log
        self.archive_id = archive_id
        self.view_id = view_id
        self.account = ''
        self.name = ''


class TestInterfaceCase(ParametrizedTestCase):
    def setUp(self):
        pass

    def test_default_normal(self, get_png=False):
        if "GET" == self.test_data.http_method:
            return_msg = self.http.get(self.test_data.request_url, self.test_data.request_param, get_png)
        elif "POST" == self.test_data.http_method:
            return_msg = self.http.post(self.test_data.request_url, self.test_data.request_param)
            # post data with form
            # return_msg = self.http.post_form(self.test_data.request_url, self.test_data.request_param)
        else:
            return_msg = ['NULL', {}]
        response_code, response = return_msg[:]
        if '000' == response_code:
            self.test_data.result = 'Error'
            desc = '{}'.format(response).replace("'", "\\'")
            response = {}
        else:
            self.log.debug(response.get("result"))
            if int(response_code) == int(self.test_data.except_code) and response.get("result") == "success":
                self.test_data.result = 'Pass'
                desc = 'NULL'
            else:
                self.test_data.result = 'Fail'
                desc = response.get("result")
            response = json.dumps(response).replace("'", "\\'")

        self.log.debug(
            "++++++++++++++++++\n result => {}\n case_id => {}\n++++++++++++++++++".format(self.test_data.result,
                                                                                           self.test_data.case_id))
        self.log.debug(type(response))
        response = '{}'.format(response.replace("'", "\'"))
        self.log.debug(response)
        self.db_cursor.insert_values(
            '''insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},"{}",{},'{}','{}','{}')'''.format(
                self.view_id,
                self.test_data.case_id,
                eval(self.test_data.request_param),
                response_code,
                response,
                # json.loads(response),
                # str(response.replace("\\","")),
                self.test_data.result,
                desc.replace("'", "\\'")
            ))

    def test_pay_wx_check(self):
        db_cursor = self.db_cursor.run_sql(
            "select t.result, t.actual_response from usercase u, test_result t where u.case_name = '/api/v0/pay_wx_create' and t.case_number = u.case_number and t.view_id = {} ".format(
                self.view_id))
        tmp_result = db_cursor.fetchall()[:]
        self.log.info(tmp_result)
        case_result = tmp_result[0][0]
        case_response = tmp_result[0][1]
        if "Pass" == case_result:
            order_no = eval(case_response).get("order_no")
            self.test_data.request_param = eval(self.test_data.request_param)
            self.test_data.request_param["order_no"] = order_no
            self.test_data.request_param = str(self.test_data.request_param)
            self.test_default_normal(True)
            return
        else:
            self.test_data.result = 'Fail'
            response_code, response = ('NULL', {})[:]
            desc = 'can not find order sms message'
            self.log.error(desc)
        self.db_cursor.insert_values(
            '''insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},"{}",{},'{}','{}','{}')'''.format(
                self.view_id,
                self.test_data.case_id,
                self.test_data.request_param,
                response_code,
                json.dumps(response),
                self.test_data.result,
                desc
            ))

    def test_qr_image(self):
        db_cursor = self.db_cursor.run_sql(
            "select t.result, t.actual_response from usercase u, test_result t where u.case_name = '/api/v0/pay_wx_create' and t.case_number = u.case_number and t.view_id = {}".format(
                self.view_id))
        tmp_result = db_cursor.fetchall()[:]
        self.log.info(tmp_result)
        if len(tmp_result) == 0:
            self.test_data.result = "Fail"
            desc = "can not find order number"
            self.log.error(desc)
            response_code = 'NULL'
            response = {}
        else:
            case_result = tmp_result[0][0]
            case_response = tmp_result[0][1]
            if "Pass" == case_result:
                pay_uri = eval(case_response).get("pay_uri")
                self.test_data.request_param = eval(self.test_data.request_param)
                self.test_data.request_param["uri"] = pay_uri
                self.test_data.request_param = str(self.test_data.request_param)
                self.test_default_normal()
                return
            else:
                self.test_data.result = 'Fail'
                response_code, response = ('NULL', {})[:]
                desc = 'can not find order sms message'
                self.log.error(desc)
            self.db_cursor.insert_values(
                '''insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},"{}",{},'{}','{}','{}')'''.format(
                    self.view_id,
                    self.test_data.case_id,
                    self.test_data.request_param,
                    response_code,
                    json.dumps(response),
                    self.test_data.result,
                    desc
                ))

    def test_sms_normal(self):
        self.log.info(self.test_data.request_param)
        db_cursor = self.db_cursor.run_sql(
            "select t.result, t.actual_response from usercase u, test_result t where u.case_name = '/api/v0/captcha/image' and t.case_number = u.case_number and t.view_id = {}".format(
                self.view_id))
        tmp_result = db_cursor.fetchall()[:]
        self.log.info(tmp_result)
        if len(tmp_result) > 0:
            case_result = tmp_result[0][0]
            case_response = tmp_result[0][1]
            if "Pass" == case_result:
                pay_uri = eval(case_response).get("code")
                self.test_data.request_param = eval(self.test_data.request_param)
                self.test_data.request_param["captcha_image"] = pay_uri
                self.test_data.request_param["phone_no"] = "110{}".format(
                    "".join(choice(string.digits) for i in range(randint(9, 9))))
                self.test_data.request_param = str(self.test_data.request_param)
                self.test_default_normal()
                return
            else:
                self.test_data.result = 'Fail'
                response_code, response = ('NULL', {})[:]
                desc = 'can not find order number'
                self.log.error(desc)
            self.db_cursor.insert_values(
                '''insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},"{}",{},'{}','{}','{}')'''.format(
                    self.view_id,
                    self.test_data.case_id,
                    self.test_data.request_param,
                    response_code,
                    json.dumps(response),
                    self.test_data.result,
                    desc
                ))


    def test_register_normal(self):
        self.log.debug(self.test_data.request_param)
        db_cursor = self.db_cursor.run_sql(
            "select t.result, t.actual_response, t.queryparameters from usercase u, test_result t where u.case_name = '/api/v0/captcha/sms' and t.case_number = u.case_number and t.view_id = {}".format(
                self.view_id))
        tmp_result = db_cursor.fetchall()[:]
        self.log.debug('got result {}'.format(tmp_result))
        if len(tmp_result) == 0:
            self.test_data.result = 'Fail'
            response_code, response = ['NULL', {}][:]
            desc = 'can not find order sms message'
            self.log.error(desc)
        else:
            case_result = tmp_result[0][0]
            case_response = tmp_result[0][1]
            case_request = tmp_result[0][2]
            if "Pass" == case_result:
                self.test_data.request_param = eval(self.test_data.request_param)
                self.test_data.request_param["phone_no"] = eval(case_request).get("phone_no")
                self.test_data.request_param["account"] = "test_{}".format(self.test_data.request_param.get("phone_no"))
                self.test_data.request_param["captcha_sms"] = eval(case_response).get("code")
                self.test_data.request_param = str(self.test_data.request_param)
                self.test_default_normal()
                return
            else:
                self.test_data.result = 'Fail'
                response_code, response = ('NULL', {})[:]
                desc = 'can not find order sms message'
                self.log.error(desc)
            self.db_cursor.insert_values(
                '''insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},"{}",{},'{}','{}','{}')'''.format(
                    self.view_id,
                    self.test_data.case_id,
                    self.test_data.request_param,
                    response_code,
                    json.dumps(response),
                    self.test_data.result,
                    desc
                ))


    def test_upload_img(self):
        self.log.info(self.test_data.request_param)
        img_path = eval(self.test_data.request_param).get("img")
        self.log.debug("test upload file path:{}".format(img_path))
        if os.path.exists(img_path):
            if "POST" == self.test_data.http_method:
                return_msg = self.http.post_file(self.test_data.request_url, img_path)
            else:
                desc = 'wrong method,upload img must be POST'
                self.log.error(desc)
                return_msg = ['NULL', {}]
            response_code, response = return_msg[:]
            if '000' == response_code:
                self.test_data.result = 'Error'
                desc = 'NULL'
            else:
                response_code, response = return_msg[:]
                self.log.debug(eval(response).get("result"))
                if int(response_code) == int(self.test_data.except_code) and eval(response).get("result") == "success":
                    self.test_data.result = 'Pass'
                    desc = 'NULL'
                else:
                    self.test_data.result = 'Error'
                    desc = 'NULL'
        else:
            self.test_data.result = 'Error'
            desc = 'img file do not exist'
            response_code, response = ['NULL', {}][:]

        self.db_cursor.insert_values(
            '''insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},"{}",{},'{}','{}','{}')'''.format(
                self.view_id,
                self.test_data.case_id,
                {},
                response_code,
                json.dumps(response),
                self.test_data.result,
                desc
            ))

    def test_login_normal(self):
        self.http.install_cookies()
        db_cursor = self.db_cursor.run_sql(
            "select t.result, t.queryparameters from usercase u, test_result t where u.case_name = '/api/v0/user/register' and t.case_number = u.case_number and t.view_id = {}".format(
                self.view_id))
        tmp_result = db_cursor.fetchall()[:]
        self.log.debug('got result {}'.format(tmp_result))
        if len(tmp_result) == 0:
            self.test_data.result = 'Fail'
            response_code, response = ['NULL', {}][:]
            desc = 'can not find a new regiser user'
            self.log.error(desc)
        else:
            if 'Pass' == tmp_result[0][0]:
                register_para = tmp_result[0][1]
                self.test_data.request_param = eval(self.test_data.request_param)
                self.test_data.request_param["user"] = eval(register_para).get("account")
                self.test_data.request_param["password"] = eval(register_para).get("password")
                # 将参数转换成字符，便于调用方便
                self.test_data.request_param = str(self.test_data.request_param)
                self.test_default_normal()
                return
            else:
                self.test_data.result = 'Fail'
                response_code, response = ('NULL', {})[:]
                desc = 'can not find order sms message'
                self.log.error(desc)
            self.db_cursor.insert_values(
                '''insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},"{}",{},'{}','{}','{}')'''.format(
                    self.view_id,
                    self.test_data.case_id,
                    self.test_data.request_param,
                    response_code,
                    json.dumps(response),
                    self.test_data.result,
                    desc
                ))

    def test_org_user_info(self):
        db_cursor = self.db_cursor.run_sql(
            "select t.result, t.actual_response from usercase u, test_result t where u.case_name = '/api/v0/user/info' and t.case_number = u.case_number and t.view_id = {}".format(
                self.view_id))
        tmp_result = db_cursor.fetchall()[:]
        self.log.debug('got result {}'.format(tmp_result))
        if len(tmp_result) == 0:
            self.test_data.result = 'Fail'
            response_code, response = ['NULL', {}][:]
            desc = 'can not find a new regiser user'
            self.log.error(desc)
        else:
            if 'Pass' == tmp_result[0][0]:
                user_info = tmp_result[0][1].replace('null', 'None').replace('false', 'False')
                self.log.debug(user_info)
                self.test_data.request_param = eval(self.test_data.request_param)
                self.test_data.request_param["number"] = eval(user_info).get("user").get('number')
                self.test_data.request_param = str(self.test_data.request_param)
                self.test_default_normal()
                return
            else:
                self.test_data.result = 'Fail'
                response_code, response = ('NULL', {})[:]
                desc = 'can not find order sms message'
                self.log.error(desc)
        self.db_cursor.insert_values(
            '''insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},"{}",{},'{}','{}','{}')'''.format(
                self.view_id,
                self.test_data.case_id,
                self.test_data.request_param,
                response_code,
                json.dumps(response),
                self.test_data.result,
                desc
            ))

    def test_org_user_update(self):
        db_cursor = self.db_cursor.run_sql(
            "select t.result, t.actual_response from usercase u, test_result t where u.case_name = '/api/v0/org/user/info' and t.case_number = u.case_number and t.view_id = {}".format(
                self.view_id))
        tmp_result = db_cursor.fetchall()[:]
        self.log.debug('got result {}'.format(tmp_result))
        if len(tmp_result) == 0:
            self.test_data.result = 'Fail'
            response_code, response = ['NULL', {}][:]
            desc = 'can not find a new regiser user'
            self.log.error(desc)
        else:
            if 'Pass' == tmp_result[0][0]:
                user_info = tmp_result[0][1].replace('null', "None").replace('false', 'False')
                self.test_data.request_param = eval(user_info).get("user")
                self.test_data.request_param["authenticated"] = 1
                self.test_data.request_param = str(self.test_data.request_param)
                self.test_default_normal()
                return
            else:
                self.test_data.result = 'Fail'
                response_code, response = ('NULL', {})[:]
                desc = 'can not find order sms message'
                self.log.error(desc)
        self.db_cursor.insert_values(
            '''insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},"{}",{},'{}','{}','{}')'''.format(
                self.view_id,
                self.test_data.case_id,
                self.test_data.request_param,
                response_code,
                json.dumps(response),
                self.test_data.result,
                desc
            ))

    def test_org_user_finance(self):
        db_cursor = self.db_cursor.run_sql(
            "select t.result, t.actual_response from usercase u, test_result t where u.case_name = '/api/v0/org/user/info' and t.case_number = u.case_number and t.view_id = {}".format(
                self.view_id))
        tmp_result = db_cursor.fetchall()[:]
        self.log.debug('got result {}'.format(tmp_result))
        if len(tmp_result) == 0:
            self.test_data.result = 'Fail'
            response_code, response = ['NULL', {}][:]
            desc = 'can not find a new regiser user'
            self.log.error(desc)
        else:
            if 'Pass' == tmp_result[0][0]:
                user_info = tmp_result[0][1].replace('null', "None").replace('false', 'False')
                self.test_data.request_param = eval(self.test_data.request_param)
                self.test_data.request_param["number"] = eval(user_info).get("user").get("number")
                self.test_data.request_param = str(self.test_data.request_param)
                self.test_default_normal()
                return
            else:
                self.test_data.result = 'Fail'
                response_code, response = ('NULL', {})[:]
                desc = 'can not find order sms message'
                self.log.error(desc)
        self.db_cursor.insert_values(
            '''insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},"{}",{},'{}','{}','{}')'''.format(
                self.view_id,
                self.test_data.case_id,
                self.test_data.request_param,
                response_code,
                json.dumps(response),
                self.test_data.result,
                desc
            ))

    def test_transfer(self):
        db_cursor = self.db_cursor.run_sql(
            "select t.result, t.actual_response from usercase u, test_result t where u.case_name = '/api/v0/org/user/info' and t.case_number = u.case_number and t.view_id = {}".format(
                self.view_id))
        tmp_result = db_cursor.fetchall()[:]
        self.log.debug('got result {}'.format(tmp_result))
        if len(tmp_result) == 0:
            self.test_data.result = 'Fail'
            response_code, response = ['NULL', {}][:]
            desc = 'can not find a new regiser user'
            self.log.error(desc)
        else:
            if 'Pass' == tmp_result[0][0]:
                user_info = tmp_result[0][1].replace('null', "None").replace('false', 'False')
                self.test_data.request_param = eval(self.test_data.request_param)
                self.test_data.request_param["number"] = eval(user_info).get("user").get("number")
                self.test_data.request_param["name"] = eval(user_info).get("user").get("name")
                self.test_data.request_param = str(self.test_data.request_param)
                self.test_default_normal()
                return
            else:
                self.test_data.result = 'Fail'
                response_code, response = ('NULL', {})[:]
                desc = 'can not find order sms message'
                self.log.error(desc)
        self.db_cursor.insert_values(
            '''insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},"{}",{},'{}','{}','{}')'''.format(
                self.view_id,
                self.test_data.case_id,
                eval(self.test_data.request_param),
                response_code,
                json.dumps(response),
                self.test_data.result,
                desc
            ))

    def test_entry_op(self):
        db_cursor = self.db_cursor.run_sql(
            "select t.result, t.actual_response from usercase u, test_result t where u.case_name = '/api/v0/hash/save' and t.case_number = u.case_number and t.view_id = {}".format(
                self.view_id))
        tmp_result = db_cursor.fetchall()[:]
        self.log.debug('got result {}'.format(tmp_result))
        if len(tmp_result) == 0:
            self.test_data.result = 'Fail'
            response_code, response = ['NULL', {}][:]
            desc = 'can not find a new entry hash'
            self.log.error(desc)
        else:
            if 'Pass' == tmp_result[0][0]:
                user_info = tmp_result[0][1].replace('null', "None").replace('false', 'False')
                self.test_data.request_param = eval(self.test_data.request_param)
                self.test_data.request_param["entry_hash"] = eval(user_info).get("entry_hash")
                self.test_data.request_param = str(self.test_data.request_param)
                self.test_default_normal()
                return
            else:
                self.test_data.result = 'Fail'
                response_code, response = ('NULL', {})[:]
                desc = 'can not find a new entry hash'
                self.log.error(desc)
        self.db_cursor.insert_values(
            '''insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},"{}",{},'{}','{}','{}')'''.format(
                self.view_id,
                self.test_data.case_id,
                eval(self.test_data.request_param),
                response_code,
                json.dumps(response),
                self.test_data.result,
                desc
            ))

    def tearDown(self):
        pass
