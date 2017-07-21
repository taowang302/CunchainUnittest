#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import datetime
import unittest

from runcase import RunCase
from globalconfig import Global
from htmlreport import HtmlReport

if __name__ == '__main__':

    start_time = datetime.datetime.now()
    global_config = Global()
    run_mode = global_config.get_run_mode() 
    run_case_list = global_config.get_run_case_list()  
    db1_conn = global_config.get_db1_conn()   

    log = global_config.get_log()
    output_dir = global_config.get_output_dir()
    archive_id =  global_config.get_run_archive_id()
    http = global_config.get_http(archive_id)
    runner = unittest.TextTestRunner()
    case_runner = RunCase()
    case_runner.run_case(runner, run_mode, run_case_list, db1_conn, http, log, archive_id)
    end_time = datetime.datetime.now()
    
    html_report = HtmlReport(db1_conn.cursor(),log)
    html_report.set_time_took(str(end_time - start_time)) 
    html_report.generate_html('test report', output_dir)
    global_config.clear()
