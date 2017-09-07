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


class TestInterfaceCase(ParametrizedTestCase):
    def setUp(self):
        pass

    def test_default_normal(self):
        if "GET" == self.test_data.http_method:
            return_msg = self.http.get(self.test_data.request_url, self.test_data.request_param)
        elif "POST" == self.test_data.http_method:
            return_msg = self.http.post(self.test_data.request_url, self.test_data.request_param)
        response_code, response = return_msg[:]
        if '000' == response_code:
            self.test_data.result = 'Error'
            response = '{}'.format(response).replace("'", "\\'")
        else:
            self.log.debug(response.get("result"))
            if int(response_code) == int(self.test_data.except_code) and response.get("result") == "success":
                self.test_data.result = 'Pass'
                desc = 'NULL'
            else:
                self.test_data.result = 'Fail'
                desc = response.get("result")
            response = json.dumps(response).replace("'", "\\'")
        try:
            self.log.debug(
                "++++++++++++++++++\n result => {}\n case_id => {}\n++++++++++++++++++".format(self.test_data.result,
                                                                                               self.test_data.case_id))
            self.db_cursor.run_sql(
                "insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},'{}',{},'{}','{}','{}')".format(
                    self.view_id,
                    self.test_data.case_id,
                    self.test_data.request_param,
                    response_code,
                    response,
                    self.test_data.result,
                    desc
                    ))


        # self.db_cursor.runsql(
        #          'UPDATE test_result SET result = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
        #              self.test_data.result, self.test_data.case_id, self.archive_id))
        #      self.db_cursor.runsql('commit')
        # except Exception as e:
        #      self.log.error('------\n{}'.format(e))
        #      self.db_cursor.runsql('rollback')
        # except :
        #      self.log.error(sys.exc_info()[1])
        # try:
        #      self.log.debug(response)
        #      # self.log.debug('UPDATE test_result SET actual_response="{}" where case_number={}'.format(json.dumps(response),self.test_data.case_id))
        #      self.db_cursor.runsql(
        #          "UPDATE test_result SET actual_response_code={} where case_number={} and from_view_id = '{}'".format(response_code, self.test_data.case_id, self.archive_id))
        #      if 'Error' == self.test_data.result:
        #          self.db_cursor.runsql(
        #          "UPDATE test_result SET description='{}' where case_number={} and from_view_id = '{}' ".format(response, self.test_data.case_id, self.archive_id))
        #      else:
        #          self.db_cursor.runsql(
        #          "UPDATE test_result SET actual_response='{}' where case_number={} and from_view_id = '{}' ".format(response, self.test_data.case_id, self.archive_id))
        #      self.db_cursor.runsql('commit')
        except Exception as e:
            self.db_cursor.run_sql('rollback')
            self.log.error(e)
        else:
            self.db_cursor.run_sql('commit')
        return

    def test_pay_wx_check(self):
        db_cursor = self.db_cursor.run_sql(
            "select t.result,t.actual_response from test_result t, usercase u where u.case_name='/api/v0/pay_wx/create' and t.case_number = u.case_number and t.from_view_id=u.from_view_id and u.from_view_id='{}' ".format(
                self.archive_id))
        tmp_result = db_cursor.fetchall()[:]
        self.log.info(tmp_result)
        case_result = tmp_result[0][0]
        case_response = tmp_result[0][1]
        if "Pass" == case_result:
            order_no = eval(case_response).get("order_no")
            self.test_data.request_param = eval(self.test_data.request_param)
            self.test_data.request_param["order_no"] = order_no
            self.test_data.request_param = str(self.test_data.request_param)
            if "GET" == self.test_data.http_method:
                return_msg = self.http.get(self.test_data.request_url, self.test_data.request_param)
            elif "POST" == self.test_data.http_method:
                return_msg = self.http.post(self.test_data.request_url, self.test_data.request_param)
            response_code, response = return_msg[:]
            if '000' == response_code:
                self.test_data.result = 'Error'
                desc = 'NULL'
            elif int(response_code) == int(self.test_data.except_code) and response.get("result") == "success":
                self.test_data.result = 'Pass'
                desc = 'NULL'
            else:
                self.test_data.result = "Fail"
                desc = response.get("result")
        else:
            self.test_data.result = "Fail"
            desc = "can not find order number"
            self.log.error(desc)
            response_code = '000'
            response = json.loads('{}')

        try:
            self.db_cursor.run_sql(
                "insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},'{}',{},'{}','{}','{}')".format(
                    self.view_id,
                    self.test_data.case_id,
                    self.test_data.request_param,
                    response_code,
                    response,
                    self.test_data.result,
                    desc
                ))

        #
        #     self.db_cursor.runsql(
        #         'UPDATE test_result SET description = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
        #             "Can not find a valid order number", self.test_data.case_id, self.archive_id))
        # try:
        #     self.log.info(response)
        #     self.db_cursor.runsql(
        #         'UPDATE test_result SET result = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
        #             self.test_data.result, self.test_data.case_id, self.archive_id))
        #     self.db_cursor.runsql(
        #         "UPDATE test_result SET actual_response_code={} where case_number={} and from_view_id = '{}'".format(
        #             response_code, self.test_data.case_id, self.archive_id))
        #     self.db_cursor.runsql(
        #         "UPDATE test_result SET actual_response='{}' where case_number={} and from_view_id = '{}' ".format(
        #             json.dumps(response), self.test_data.case_id, self.archive_id))
        #     self.db_cursor.runsql('commit')
        except Exception as e:
            self.db_cursor.run_sql('rollback')
            self.log.error(e)
        else:
            self.db_cursor.run_sql('commit')
        return

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
                if "GET" == self.test_data.http_method:
                    return_msg = self.http.get(self.test_data.request_url, self.test_data.request_param, True)
                elif "POST" == self.test_data.http_method:
                    return_msg = self.http.post(self.test_data.request_url, self.test_data.request_param)
                else:
                    self.log.error(
                        "do not support this method:{},please use POST or GET".format(self.test_data.http_method))
                    return_msg = ['000', {}]
                    desc = 'error http method'
                if '000' == return_msg[0]:
                    self.test_data.result = 'Error'
                    desc = 'NULL'
                else:
                    response_code, response = return_msg[:]
                    if int(response_code) == int(self.test_data.except_code):
                        self.test_data.result = 'Pass'
                        desc = 'NULL'
                    else:
                        self.test_data.result = 'Fail'
                        desc = 'NULL'
            else:
                self.test_data.result = "Fail"
                desc = "can not find order number"
                self.log.error(desc)
                response_code = '000'
                response = json.loads('{}')

        self.db_cursor.insert_values(
            "insert into test_result (view_id, case_number, queryparameters, actual_response_code, actual_response, result, description) values({},{},'{}',{},'{}','{}','{}')".format(
                self.view_id,
                self.test_data.case_id,
                self.test_data.request_param,
                response_code,
                response,
                self.test_data.result,
                desc
            ))
        #     try:
        #         self.db_cursor.runsql(
        #             'UPDATE test_result SET result = "{}",actual_response_code = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
        #                 self.test_data.result, response_code, self.test_data.case_id, self.archive_id))
        #         if "Error" != self.test_data.result:
        #             self.db_cursor.runsql(
        #                 "UPDATE test_result SET actual_response='{}' where case_number={} and from_view_id = '{}' ".format(
        #                 json.dumps(response), self.test_data.case_id, self.archive_id))
        #         else:
        #             self.db_cursor.runsql(
        #                 "UPDATE test_result SET description='{}' where case_number={} and from_view_id = '{}' ".format(
        #                     self.test_data.result, response_code, self.test_data.case_id, self.archive_id))
        #         self.db_cursor.runsql('commit')
        #     except:
        #         self.log.error(sys.exc_info[1])
        #     return
        # else:
        #     self.log.error("can not find order number")
        #     self.db_cursor.runsql(
        #         'UPDATE test_result SET actual_response_code = "000",result = "{}" WHERE case_number = {} and from_view_id = "{}"'.format("Fail",
        #                                                                                                      self.test_data.case_id,
        #                                                                                                      self.archive_id))
        #     self.db_cursor.runsql(
        #         'UPDATE test_result SET description = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
        #             "Can not find a valid order number", self.test_data.case_id, self.archive_id))
        #     self.db_cursor.runsql('commit')
        # return

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
                if "GET" == self.test_data.http_method:
                    return_msg = self.http.get(self.test_data.request_url, self.test_data.request_param)
                    self.log.info(self.test_data.request_param)
                elif "POST" == self.test_data.http_method:
                    return_msg = self.http.post(self.test_data.request_url, self.test_data.request_param)
                    self.log.info(self.test_data.request_param)
                else:
                    self.log.error(
                        "do not support this method:{},please use POST or GET".format(self.test_data.http_method))
                    return_msg = ['000', {}]
                response_code, response = return_msg[:]
                if '000' == response_code:
                    self.test_data.result = 'Error'
                    desc = 'NULL'
                else:
                    if int(response_code) == int(self.test_data.except_code):
                        self.test_data.result = 'Pass'
                        desc = 'NULL'
                    else:
                        self.test_data.result = 'Fail'
                        desc = 'NULL'
            else:
                self.test_data.result = 'Fail'
                self.log.error('can not find order number')
                response_code = 'NULL'
                response = 'NULL'
                desc = 'can not find order number'
        else:
            self.test_data.result = 'Fail'
            self.log.error('can not find order number')
            response_code = 'NULL'
            response = 'NULL'
            desc = 'can not find order number'
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
        #         try:
        #             self.db_cursor.runsql(
        #                 'UPDATE usercase SET queryparameters = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
        #                      self.test_data.request_param, self.test_data.case_id, self.archive_id))
        #             self.db_cursor.runsql(
        #                 'UPDATE test_result SET result = "{}",actual_response_code = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
        #                     self.test_data.result, response_code, self.test_data.case_id, self.archive_id))
        #             if "Error" != self.test_data.result:
        #                 self.db_cursor.runsql(
        #                     "UPDATE test_result SET actual_response='{}' where case_number={} and from_view_id = '{}' ".format(
        #                     json.dumps(response), self.test_data.case_id, self.archive_id))
        #             else:
        #                 self.db_cursor.runsql(
        #                     "UPDATE test_result SET description='{}' where case_number={} and from_view_id = '{}' ".format(
        #                         self.test_data.result, response_code, self.test_data.case_id, self.archive_id))
        #             self.db_cursor.runsql('commit')
        #         except:
        #             self.log.error(sys.exc_info[1])
        #         return
        # else:
        #     self.log.error("can not find valid captcha_image")
        #     try:
        #         self.db_cursor.runsql(
        #             'UPDATE test_result SET result = "Error",actual_response_code = "000" WHERE case_number = {} and from_view_id = "{}"'.format(self.test_data.case_id, self.archive_id))
        #         self.db_cursor.runsql(
        #             "UPDATE test_result SET description='{}' where case_number={} and from_view_id = '{}' ".format(
        #                 "can not find order valid captcha_image message", self.test_data.case_id, self.archive_id))
        #         self.db_cursor.runsql('commit')
        #     except:
        #         self.log.error(sys.exc_info[1])
        #

    def test_register_normal(self):
        self.log.debug(self.test_data.request_param)
        db_cursor = self.db_cursor.run_sql(
            "select t.result, t.actual_response from usercase u, test_result t where u.case_name = '/api/v0/captcha/sms' and t.case_number = u.case_number and t.view_id = {}".format(
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
                if "GET" == self.test_data.http_method:
                    return_msg = self.http.get(self.test_data.request_url, self.test_data.request_param)
                elif "POST" == self.test_data.http_method:
                    return_msg = self.http.post(self.test_data.request_url, self.test_data.request_param)
                else:
                    self.log.error(
                        "do not support this method:{},please use POST or GET".format(self.test_data.http_method))
                    self.test_data.result = 'Fail'
                    return_msg = ('NULL, {}')
                    desc = 'do not support this method'
                response_code, response = return_msg[:]
                if '000' == response_code:
                    self.test_data.result = 'Error'
                    desc = 'NULL'
                else:
                    if int(response_code) == int(self.test_data.except_code):
                        self.test_data.result = 'Pass'
                        desc = 'NULL'
                    else:
                        self.test_data.result = 'Fail'
                        desc = 'NULL'
            else:
                self.test_data.result = 'Fail'
                response_code, response = ('NULL, {}')
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
        #
        #
        #
        #     try:
        #         self.log.debug("++++++++++++++++++\n result => {}\n case_id => {}\n++++++++++++++++++".format(self.test_data.result,self.test_data.case_id))
        #
        #
        #
        #         self.db_cursor.runsql(
        #             'UPDATE test_result SET result = "{}",actual_response_code={} WHERE case_number = {} and from_view_id = "{}"'.format(
        #                 self.test_data.result, response_code,self.test_data.case_id, self.archive_id))
        #         if "Error" != self.test_data.result:
        #             self.db_cursor.runsql(
        #                 "UPDATE test_result SET actual_response='{}' where case_number={} and from_view_id = '{}' ".format(
        #                 json.dumps(response), self.test_data.case_id, self.archive_id))
        #         else:
        #             self.db_cursor.runsql(
        #                 "UPDATE test_result SET description='{}' where case_number={} and from_view_id = '{}' ".format(
        #                     self.test_data.result, response_code, self.test_data.case_id, self.archive_id))
        #         self.db_cursor.runsql('commit')
        #     except:
        #         self.log.error("Found err:{}".format(sys_exc_info()[1]))
        # else:
        #     slef.log.error("Upload file do not found:{}".format(img_path))
        #     self.db_cursor.runsql(
        #         'UPDATE test_result SET result = "{}" WHERE case_number = {} and from_view_id = "{}"'.format("Error",
        #                                                                                                      self.test_data.case_id,
        #                                                                                                      self.archive_id))
        #     self.db_cursor.runsql(
        #         'UPDATE test_result SET description = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
        #             "Not found the image", self.test_data.case_id, self.archive_id))
        # return

    def test_login_normal(self):
        response = self.http.get(self.test_data.request_url, self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                self.cursor.runsql('UPDATE test_result SET result = %s WHERE case_id = %s',
                                   (self.test_data.result, self.test_data.case_id))
                self.cursor.runsql('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.runsql('rollback')
            return

        try:
            db2_cursor = self.db2_cursor.runsql('SELECT user_id FROM 1dcq_user WHERE mobile = %s',
                                                (eval(self.test_data.request_param)['mobile'],))
            user_id = self.db2_cursor.fetchone()[0]
            self.db2_cursor.close()
            self.assertEqual(response['code'], 0, msg='返回code不等于0')
            self.assertEqual(response['msg'], '登录成功', msg='登录失败')
            self.assertEqual(response['data']['sex'], 2, msg='sex错误')
            self.assertEqual(response['data']['cityId'], None, msg='cityId错误')
            self.assertEqual(response['data']['nikeName'], None, msg='nikeName错误')
            self.assertEqual(response['data']['cityName'], None, msg='cityName错误')
            self.assertEqual(response['data']['userId'], user_id, msg='userId错误')  # 2910057590
            self.assertEqual(response['data']['cityName'], None, msg='cityName错误')
            self.assertEqual(response['data']['payPasswordFlag'], 1, msg='payPasswordFlag错误')
            self.assertEqual(response['data']['imgSmall'], None, msg='imgSmall错误')
            self.assertEqual(response['data']['imgBig'], None, msg='imgBig错误')
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' % e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' % e  # 记录失败原因

        try:
            self.db_cursor.runsql('UPDATE test_result SET result = %s WHERE case_id = %s',
                                  (self.test_data.result, self.test_data.case_id))
            self.db_cursor.runsql('UPDATE test_result SET reason = %s WHERE case_id = %s',
                                  (self.test_data.reason, self.test_data.case_id))
            self.db_cursor.runsql('commit')
        except Exception as e:
            print('%s' % e)
            self.db_cursor.runsql('rollback')

    def test_chpasswd_normal(self):
        header = {'Content-Type': 'application/json', 'charset': 'utf-8'}
        self.http.set_header(header)
        self.db_cursor.runsql('SELECT request_url, request_param FROM pre_condition_data WHERE case_id = %s and step=1',
                              (self.test_data.case_id,))
        temp_result = self.db_cursor.fetchone()
        request_url = temp_result[0]
        request_param = temp_result[1]
        lgin_response = self.http.get(request_url, request_param)

        user_id = lgin_response['data']['userId']  # 获取登录接口返回的user_id
        payPassword = eval(request_param)['password']  # 获取原密码即登录密码

        tmp_dic = {"userId": user_id, "payPassword": payPassword}
        self.test_data.request_param = eval(self.test_data.request_param)
        self.test_data.request_param.update(tmp_dic)

        response = self.http.post(self.test_data.request_url, str(self.test_data.request_param))

        if {} == response:
            self.test_data.result = 'Error'
            try:
                self.db_cursor.runsql('UPDATE test_result SET result = %s WHERE case_id = %s',
                                      (self.test_data.result, self.test_data.case_id))
                self.db_cursor.runsql('commit')
            except Exception as e:
                print('%s' % e)
                self.db_cursor.runsql('rollback')
            return
        try:
            self.assertEqual(response['code'], 0, msg='返回code不等于0')
            self.assertEqual(response['msg'], '支付密码修改成功', msg='修改支付密码失败')
            self.assertEqual(response['data'], None, msg='data不为N')
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' % e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' % e  # 记录失败原因

        try:
            self.db_cursor.runsql('UPDATE test_result SET request_param = %s WHERE case_id = %s',
                                  (str(self.test_data.request_param), self.test_data.case_id))
            self.db_cursor.runsql('UPDATE test_result SET result = %s WHERE case_id = %s',
                                  (self.test_data.result, self.test_data.case_id))
            self.db_cursor.runsql('UPDATE test_result SET reason = %s WHERE case_id = %s',
                                  (self.test_data.reason, self.test_data.case_id))
            self.db_cursor.runsql('commit')
        except Exception as e:
            print('%s' % e)
            self.db_cursor.runsql('rollback')

    def tearDown(self):
        pass
