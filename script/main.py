#!/usr/bin/env python
# -*- coding:utf-8 -*-



# import datetime
import unittest

from runcase import RunCase
# from globalconfig import Global
from globalconfig import GlobalConfig
from htmlreport import HtmlReport

if __name__ == '__main__':
    # start_time = datetime.datetime.now()
    # global_config = Global()
    global_config = GlobalConfig()
    run_mode = global_config.get_run_mode() 
    run_case_list = global_config.get_run_case_list()
    db_conn = global_config.get_db_conn()

    log = global_config.get_log()
    output_dir = global_config.get_output_dir()
    archive_id =  global_config.get_run_archive_id()
    http = global_config.get_http(archive_id)
    runner = unittest.TextTestRunner()
    case_runner = RunCase()
    case_runner.run_case(runner, run_mode, run_case_list, db_conn, http, log, archive_id, output_dir)
    # end_time = datetime.datetime.now()
    #
    # html_report = HtmlReport(db_conn, log, archive_id, run_mode, run_case_list)
    # html_report.set_time_took(str(end_time - start_time))
    # html_report.generate_html('test report', output_dir)
    global_config.clear()
