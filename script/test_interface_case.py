#!/usr/bin/env python
# -*- coding:utf-8 -*-


import  unittest
import json
import os
import sys

class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """

    def __init__(self, methodName='runTest', test_data=None, http=None, db_cursor=None, db2_cursor=None, log=None,
                 archive_id=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.test_data = test_data
        self.http = http
        self.db_cursor = db_cursor
        self.db2_cursor = db2_cursor
        self.log = log
        self.archive_id = archive_id


class TestInterfaceCase(ParametrizedTestCase):
   def setUp(self):
       pass

   def test_default_normal(self):
       if "GET" == self.test_data.http_method :
           return_msg = self.http.get(self.test_data.request_url,  self.test_data.request_param)
       elif "POST" == self.test_data.http_method :
           return_msg = self.http.post(self.test_data.request_url, self.test_data.request_param)
       response_code,response = return_msg[:]
       if '000' == response_code:
            self.test_data.result = 'Error'
       else: 
            self.log.debug(response.get("result"))
            if int(response_code) == int(self.test_data.except_code) and response.get("result") == "success":
                self.test_data.result = 'Pass'
            else:
                self.test_data.result = 'Fail'
       try:
            self.log.debug("++++++++++++++++++\n result => {}\n case_id => {}\n++++++++++++++++++".format(self.test_data.result, self.test_data.case_id))
            self.db_cursor.execute(
                'UPDATE test_result SET result = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
                    self.test_data.result, self.test_data.case_id, self.archive_id))
            self.db_cursor.execute('commit')
       except Exception as e:
            self.log.error('------\n{}'.format(e))
            self.db_cursor.execute('rollback')
       except :
            self.log.error(sys.exc_info()[1])
       try:
            self.log.debug(type(response))
            self.log.debug(response)
            self.log.debug('UPDATE test_result SET actual_response="{}" where case_number={}'.format(json.dumps(response),self.test_data.case_id))
            self.db_cursor.execute(
                "UPDATE test_result SET actual_response_code={} where case_number={} and from_view_id = '{}'".format(
                    response_code, self.test_data.case_id, self.archive_id))
            self.db_cursor.execute(
                "UPDATE test_result SET actual_response='{}' where case_number={} and from_view_id = '{}' ".format(
                    json.dumps(response).replace("'", "\\'"), self.test_data.case_id, self.archive_id))
            self.db_cursor.execute('commit')
       except Exception as e:
           self.log.error(e)
       return

   def test_pay_wx_check(self):
       self.db_cursor.execute(
           "select t.result,t.actual_response from test_result t, usercase u where u.case_name='/api/v0/pay_wx/create' and t.case_number = u.case_number and t.from_view_id=u.from_view_id and u.from_view_id='{}' ".format(
               self.archive_id))
       tmp_result = self.db_cursor.fetchall()[:]
       self.log.info(tmp_result)
       case_result = tmp_result[0][0]
       case_response = tmp_result[0][1]
       if "Pass" == case_result:
           order_no = eval(case_response).get("order_no")
           self.test_data.request_param=eval(self.test_data.request_param)
           self.test_data.request_param["order_no"] = order_no
           self.test_data.request_param=str(self.test_data.request_param)
           if "GET" == self.test_data.http_method :
               return_msg = self.http.get(self.test_data.request_url,  self.test_data.request_param)
           elif "POST" == self.test_data.http_method :
               return_msg = self.http.post(self.test_data.request_url,  self.test_data.request_param)
           response_code,response = return_msg[:]
           if '000' == response_code:
                self.test_data.result = 'Error'
           elif int(response_code) == int(self.test_data.except_code) and response.get("result") == "success":
                self.test_data.result = 'Pass'
           else:
                self.test_data.result = "Fail"
       else:
           self.test_data.result = "Fail"
           self.log.error("can not find order number")
           response_code='000'
           response=json.loads('{}')
           self.db_cursor.execute(
               'UPDATE test_result SET description = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
                   "Can not find a valid order number", self.test_data.case_id, self.archive_id))
       try:
           self.log.debug(type(response))
           self.log.info(response)
           self.db_cursor.execute(
               'UPDATE test_result SET result = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
                   self.test_data.result, self.test_data.case_id, self.archive_id))
           self.db_cursor.execute(
               "UPDATE test_result SET actual_response_code={} where case_number={} and from_view_id = '{}'".format(
                   response_code, self.test_data.case_id, self.archive_id))
           self.db_cursor.execute(
               "UPDATE test_result SET actual_response='{}' where case_number={} and from_view_id = '{}' ".format(
                   json.dumps(response), self.test_data.case_id, self.archive_id))
           self.db_cursor.execute('commit')
       except Exception as e:
                self.log.error('%s' % e)
       return

   def test_qr_image(self):
       self.db_cursor.execute(
           "select t.result,t.actual_response from test_result t, usercase u where u.case_name='/api/v0/pay_wx/create' and t.case_number = u.case_number and u.from_view_id='{}' and u.from_view_id=t.from_view_id".format(
               self.archive_id))
       tmp_result = self.db_cursor.fetchall()[:]
       self.log.info(tmp_result)
       case_result = tmp_result[0][0]
       case_response = tmp_result[0][1]
       if "Pass" == case_result:
           pay_uri = eval(case_response).get("pay_uri")
           self.test_data.request_param=eval(self.test_data.request_param)
           self.test_data.request_param["uri"] = pay_uri
           self.test_data.request_param=str(self.test_data.request_param)
           if "GET" == self.test_data.http_method :
               return_msg = self.http.get(self.test_data.request_url,  self.test_data.request_param,True)
           elif "POST" == self.test_data.http_method :
               return_msg = self.http.post(self.test_data.request_url,  self.test_data.request_param)
           else:
               self.log.error("do not support this method:{},please use POST or GET".format(self.test_data.http_method))
           if '000' == return_msg[0]:
                self.test_data.result = 'Error'
           else:
               response_code, response = return_msg[:]
               if int(response_code) == int(self.test_data.except_code): 
                   self.test_data.result = 'Pass'
               else:
                   self.test_data.result = 'Error'
           try:
               self.db_cursor.execute(
                   'UPDATE test_result SET result = "{}",actual_response_code = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
                       self.test_data.result, response_code, self.test_data.case_id, self.archive_id))
               self.db_cursor.execute(
                   "UPDATE test_result SET actual_response='{}' where case_number={} and from_view_id = '{}' ".format(
                       json.dumps(response), self.test_data.case_id, self.archive_id))
               self.db_cursor.execute('commit')
           except:
               self.log.error('sys.exc_info[1]')
           return
       else:
           self.log.error("can not find order number")
           self.db_cursor.execute(
               'UPDATE test_result SET actual_response_code = "000",result = "{}" WHERE case_number = {} and from_view_id = "{}"'.format("Fail",
                                                                                                            self.test_data.case_id,
                                                                                                            self.archive_id))
           self.db_cursor.execute(
               'UPDATE test_result SET description = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
                   "Can not find a valid order number", self.test_data.case_id, self.archive_id))
           self.db_cursor.execute('commit')
       return

   def test_upload_img(self):
       self.log.info(self.test_data.request_param)
       img_path = eval(self.test_data.request_param).get("img")
       self.log.debug("test upload file path:{}".format(img_path))
       if os.path.exists(img_path):
           if "POST" == self.test_data.http_method :
               return_msg = self.http.post_file(self.test_data.request_url, img_path)
           else:
               self.log.error("wrong method,upload img must be POST")
               return
           response_code, response = return_msg[:]
           if '000' == response_code:
               self.test_data.result = 'Error'
           else:
               response_code, response = return_msg[:]
               self.log.debug(eval(response).get("result"))
               if int(response_code) == int(self.test_data.except_code) and eval(response).get("result") == "success": 
                   self.test_data.result = 'Pass'
               else:
                   self.test_data.result = 'Error'
           try:
               self.log.debug("++++++++++++++++++\n result => {}\n case_id => {}\n++++++++++++++++++".format(self.test_data.result,self.test_data.case_id))
               self.db_cursor.execute(
                   'UPDATE test_result SET result = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
                       self.test_data.result, self.test_data.case_id, self.archive_id))
               self.db_cursor.execute('commit')
           except Exception as e:
               print('------\n{}'.format(e))
               self.db_cursor.execute('rollback')
           except:
               self.log.error("Found err:{}".format(sys_exc_info()[1]))
           try:
               self.log.debug(type(response))
               self.log.info('Get response:\n{}'.format(response))
               self.db_cursor.execute(
                   'UPDATE test_result SET actual_response_code={} where case_number={} and from_view_id = "{}"'.format(
                       response_code, self.test_data.case_id, self.archive_id))
               self.db_cursor.execute(
                   'UPDATE test_result SET actual_response="{}" where case_number={} and from_view_id = "{}"'.format(
                       eval(response), self.test_data.case_id, self.archive_id))
               self.db_cursor.execute('commit')
           except Exception as e:
               self.log.error('%s' % e)
       else:
           slef.log.error("Upload file do not found:{}".format(img_path))
           self.db_cursor.execute(
               'UPDATE test_result SET result = "{}" WHERE case_number = {} and from_view_id = "{}"'.format("Error",
                                                                                                            self.test_data.case_id,
                                                                                                            self.archive_id))
           self.db_cursor.execute(
               'UPDATE test_result SET description = "{}" WHERE case_number = {} and from_view_id = "{}"'.format(
                   "Not found the image", self.test_data.case_id, self.archive_id))
       return


   def test_login_normal(self):
       response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
       if {} == response:
            self.test_data.result = 'Error'
            try:
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s', (self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return

       try:
           self.db2_cursor.execute('SELECT user_id FROM 1dcq_user WHERE mobile = %s',(eval(self.test_data.request_param)['mobile'],))
           user_id = self.db2_cursor.fetchone()[0]
           self.db2_cursor.close()
           self.assertEqual(response['code'], 0, msg='返回code不等于0')
           self.assertEqual(response['msg'], '登录成功', msg='登录失败')
           self.assertEqual(response['data']['sex'], 2, msg='sex错误')
           self.assertEqual(response['data']['cityId'], None, msg='cityId错误')
           self.assertEqual(response['data']['nikeName'], None, msg='nikeName错误')
           self.assertEqual(response['data']['cityName'], None, msg='cityName错误')
           self.assertEqual(response['data']['userId'], user_id, msg='userId错误')  #2910057590
           self.assertEqual(response['data']['cityName'], None, msg='cityName错误')
           self.assertEqual(response['data']['payPasswordFlag'], 1, msg='payPasswordFlag错误')
           self.assertEqual(response['data']['imgSmall'], None, msg='imgSmall错误')
           self.assertEqual(response['data']['imgBig'], None, msg='imgBig错误')
           self.test_data.result = 'Pass'
       except AssertionError as e:
           print('%s' % e)
           self.test_data.result = 'Fail'
           self.test_data.reason = '%s' % e # 记录失败原因

       try:
           self.db_cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s',
                                  (self.test_data.result, self.test_data.case_id))
           self.db_cursor.execute('UPDATE test_result SET reason = %s WHERE case_id = %s',
                                  (self.test_data.reason, self.test_data.case_id))
           self.db_cursor.execute('commit')
       except Exception as e:
           print('%s' % e)
           self.db_cursor.execute('rollback')

   def test_chpasswd_normal(self):
       header = {'Content-Type':'application/json','charset':'utf-8'}
       self.http.set_header(header)
       self.db_cursor.execute('SELECT request_url, request_param FROM pre_condition_data WHERE case_id = %s and step=1',
                              (self.test_data.case_id,))
       temp_result = self.db_cursor.fetchone()
       request_url = temp_result[0]
       request_param = temp_result[1]
       lgin_response = self.http.get(request_url, request_param)

       user_id = lgin_response['data']['userId']   # 获取登录接口返回的user_id
       payPassword = eval(request_param)['password']   # 获取原密码即登录密码

       tmp_dic = {"userId":user_id, "payPassword":payPassword}
       self.test_data.request_param = eval(self.test_data.request_param)
       self.test_data.request_param.update(tmp_dic)

       response = self.http.post(self.test_data.request_url,  str(self.test_data.request_param))

       if {} == response:
            self.test_data.result = 'Error'
            try:
                self.db_cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s',
                                       (self.test_data.result, self.test_data.case_id))
                self.db_cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.db_cursor.execute('rollback')
            return
       try:
           self.assertEqual(response['code'], 0, msg='返回code不等于0')
           self.assertEqual(response['msg'],'支付密码修改成功', msg='修改支付密码失败')
           self.assertEqual(response['data'],None, msg='data不为N')
           self.test_data.result = 'Pass'
       except AssertionError as e:
           print('%s' % e)
           self.test_data.result = 'Fail'
           self.test_data.reason = '%s' % e  # 记录失败原因

       try:
           self.db_cursor.execute('UPDATE test_result SET request_param = %s WHERE case_id = %s',
                                  (str(self.test_data.request_param), self.test_data.case_id))
           self.db_cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s',
                                  (self.test_data.result, self.test_data.case_id))
           self.db_cursor.execute('UPDATE test_result SET reason = %s WHERE case_id = %s',
                                  (self.test_data.reason, self.test_data.case_id))
           self.db_cursor.execute('commit')
       except Exception as e:
           print('%s' % e)
           self.db_cursor.execute('rollback')

   def tearDown(self):
       pass
