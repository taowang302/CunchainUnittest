#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from getdb import GetDB
from confighttp import ConfigHttp
from configrunmode import ConfigRunMode
import configlog

class Global:
    def __init__(self):
        self.log = configlog.config_log('../conf/global_config.ini')
        self.http = ConfigHttp('../conf/global_config.ini',self.log)
        self.db1 = GetDB('../conf/global_config.ini', 'DATABASE1')
        #self.db2 = GetDB('../db_config.ini', 'DATABASE2')
        self.run_mode_config = ConfigRunMode('../conf/global_config.ini')
    
    def get_log(self):
        return self.log

    def get_http(self):
        return self.http
    def get_output_dir(self):
        return self.run_mode_config.get_output_dir()
    def get_db1_conn(self):
        return self.db1.get_conn()

    def get_db2_conn(self):
        return self.db2.get_conn()

    def get_run_mode(self):
        return self.run_mode_config.get_run_mode()
    def get_run_archive_id(self):
        return self.run_mode_config.get_run_archive_id()
    def get_run_case_list(self):
        return self.run_mode_config.get_case_list()

    def clear(self):
        self.db1.get_conn().close()
        #self.db2.get_conn().close()
