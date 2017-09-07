#!/usr/bin/env python
# -*- coding:utf-8 -*-


import unittest
from test_interface_case import TestInterfaceCase
from datastruct import DataStruct
from htmlreport import HtmlReport
import datetime

global test_data
test_data = DataStruct()

class  RunCase:

    def __init__(self):
        self.result_view_id = ''

    def gen_html(self, db_conn, log, view_id, run_mode, run_case_list, waste_time, output_dir):
        html_report = HtmlReport(db_conn, log, view_id, run_mode, run_case_list)
        html_report.set_time_took(str(waste_time))
        html_report.generate_html('test report', output_dir)

    def run_case(self, runner, run_mode, run_case_list, db_conn, http, log, archive_id, output_dir):
        start_time = datetime.datetime.now()
        # db_cursor = db_conn.cursor()
        db_cursor = db_conn.run_sql(
            "SELECT COUNT(file_number)  FROM file_bag where file_number='{}'".format(archive_id))
        archive_num = db_cursor.fetchone()[0]
        # db_cursor.close()
        if int(archive_num) != 1:
            log.error("Wrong archive id :[{}]".format(archive_id))
            raise ValueError("Wrong archive id :[{}]".format(archive_id))
            return
        else:
            db_cursor = db_conn.run_sql("SELECT NEXTVAL('ViewidSeq');")
            self.result_view_id = db_cursor.fetchone()[0]
            log.debug('The view id is {} this time'.format(self.result_view_id))
            db_conn.run_sql(
                "INSERT INTO case_view (from_id,to_id) VALUES('{}',{})".format(archive_id, self.result_view_id))
            db_conn.run_sql('commit')

        global test_data
        if 1 == run_mode:
            db_cursor = db_conn.run_sql(
                "SELECT COUNT(case_number)  FROM usercase where from_view_id='{}'".format(archive_id))
            test_case_num = db_cursor.fetchone()[0]
            db_cursor.close()
            for case_id in range(1, test_case_num+1):
                db_cursor = db_conn.run_sql(
                    'select t.case_name,t.http_method,t.queryparameters,f.host,r.except_response_code,r.except_response,t.test_method from usercase t,file_bag f,test_result r where f.file_number="{}" and t.case_number={} and r.from_view_id=f.file_number and f.file_number=t.from_view_id'.format(
                        archive_id, case_id))
                tmp_result = db_cursor.fetchall()[:]
                log.debug(tmp_result)
                tmp_result = tmp_result[0]
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
                log.info("Test API: {}, Method: {}".format(test_data.request_name, test_data.http_method))
                test_suite = unittest.TestSuite()
                test_suite.addTest(
                    TestInterfaceCase(test_data.test_method,
                                      test_data,
                                      http,
                                      db_conn,
                                      log=log,
                                      archive_id=archive_id,
                                      view_id=self.result_view_id))
                runner.run(test_suite)
                db_cursor.close()
                end_time = datetime.datetime.now()
                self.gen_html(db_conn, log, self.result_view_id, run_mode, run_case_list, end_time - start_time,
                              output_dir)
        elif 0 == run_mode:  
            for case_id in run_case_list:
                db_cursor = db_conn.run_sql(
                    'select t.case_name,t.http_method,t.queryparameters,f.host,t.except_response_code,t.except_response,t.test_method from usercase t,file_bag f where f.file_number="{}" and t.case_number={} and  f.file_number=t.from_view_id'.format(
                        archive_id, case_id))
                tmp_result = db_cursor.fetchall()[:]
                # log.debug(tmp_result)
                tmp_result = tmp_result[0]
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
                log.info("Test API: {}, Method: {}".format(test_data.request_name, test_data.http_method))
                test_suite = unittest.TestSuite()
                test_suite.addTest(
                    TestInterfaceCase(test_data.test_method,
                                      test_data,
                                      http,
                                      db_conn,
                                      log=log,
                                      archive_id=archive_id,
                                      view_id=self.result_view_id))
                runner.run(test_suite)
                db_cursor.close()
                end_time = datetime.datetime.now()
                self.gen_html(db_conn, log, self.result_view_id, run_mode, run_case_list, end_time - start_time,
                              output_dir)
        else:
            log.error("load a run mode")
