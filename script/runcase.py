#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import unittest
from test_interface_case import TestInterfaceCase
from datastruct import DataStruct

global test_data
test_data = DataStruct()

class  RunCase:

    def __init__(self):
        pass

    def run_case(self, runner, run_mode, run_case_list, db_conn, http, log, archive_id):
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT COUNT(file_number)  FROM file_bag where file_number='{}'".format(archive_id))
        archive_num = db_cursor.fetchone()[0]
        # db_cursor.close()
        if int(archive_num) != 1:
            log.error("Wrong archive id :[{}]".format(archive_id))
            return
        else:
            db_cursor.execute(
                "UPDATE test_result set actual_response=NULL ,result=NULL,description=Null,actual_response_code=Null where from_view_id='{}'".format(
                    archive_id))
            db_cursor.execute('commit')
            db_cursor.close()
        global test_data
        if 1 == run_mode:
            db_cursor = db_conn.cursor()
            db_cursor.execute("SELECT COUNT(case_number)  FROM usercase where from_view_id='{}'".format(archive_id))
            test_case_num = db_cursor.fetchone()[0]
            db_cursor.close()

            for case_id in range(1, test_case_num+1):
                db_cursor = db_conn.cursor()
                 #db2_cursor = db2_conn.cursor()
                db_cursor.execute(
                    'select t.case_name,t.http_method,t.queryparameters,f.host,r.except_response_code,r.except_response,t.test_method from usercase t,file_bag f,test_result r where f.file_number="{}" and t.case_number={} and r.from_view_id=f.file_number and f.file_number=t.from_view_id'.format(
                        archive_id, case_id))
                tmp_result = db_cursor.fetchall()[:]
                 log.debug(tmp_result)
                 tmp_result=tmp_result[0]
                 test_data.case_id = case_id
                 test_data.http_method = tmp_result[1]
                 test_data.request_name = tmp_result[0]
                 test_data.request_url = tmp_result[0]
                 test_data.request_param = tmp_result[2]
                 test_data.test_method = tmp_result[6]
                 test_data.except_code = tmp_result[4]
                 test_data.except_response = tmp_result[5]
                 test_data.result = ''
                 test_data.reason = ''
                 log.info("Test API: {}, Method: {}".format(test_data.request_name,test_data.http_method))
                 test_suite = unittest.TestSuite()
                test_suite.addTest(
                    TestInterfaceCase(test_data.test_method, test_data, http, db_cursor, log=log, archive_id=archive_id))
                 runner.run(test_suite)
                db_cursor.close()
        elif 0 == run_mode:  
            for case_id in run_case_list:
                db_cursor = db_conn.cursor()
                 #db2_cursor = db2_conn.cursor()
                db_cursor.execute(
                    'select t.case_name,t.http_method,t.queryparameters,f.host,r.except_response_code,r.except_response,t.test_method from usercase t,file_bag f,test_result r where f.file_number="{}" and t.case_number={} and r.from_view_id=f.file_number and f.file_number=t.from_view_id'.format(
                        archive_id, case_id))
                tmp_result = db_cursor.fetchall()[:]
                 #log.debug(tmp_result)
                 tmp_result=tmp_result[0]
                 test_data.case_id = case_id
                 test_data.http_method = tmp_result[1]
                 test_data.request_name = tmp_result[0]
                 test_data.request_url = tmp_result[0]
                 test_data.request_param = tmp_result[2]
                 test_data.test_method = tmp_result[6]
                 test_data.except_code = tmp_result[4]
                 test_data.except_response = tmp_result[5]
                 test_data.result = ''
                 test_data.reason = ''
                 log.info("Test API: {}, Method: {}".format(test_data.request_name,test_data.http_method))
                 test_suite = unittest.TestSuite()
                test_suite.addTest(
                    TestInterfaceCase(test_data.test_method, test_data, http, db_cursor, log=log, archive_id=archive_id))
                 runner.run(test_suite)
                db_cursor.close()
        else:
            log.error("load a run mode")
