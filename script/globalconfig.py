#!/usr/bin/env python
# -*- coding:utf-8 -*-


from getdb import GetDB
from confighttp import ConfigHttp
from configrunmode import ConfigRunMode
import configlog
import configparser


class GlobalConfig():
    def __init__(self):
        self.config_dic = {}
        self.read_config()
        self.log = configlog.config_log(self.config_dic.get("LOG"))
        self.debug_config()
        self.db = GetDB(self.config_dic.get('DATABASE'), self.log)
        self.run_mode_config = ConfigRunMode(self.config_dic.get("RUNCASECONFIG"))

    def read_config(self):
        config = configparser.ConfigParser()
        config.read('../conf/global_config.ini')
        for section in config.sections():
            self.config_dic[section] = dict(config.items(section))
            # print(json.dumps(self.config_dic, indent=4, sort_keys=False, ensure_ascii=False))

    def debug_config(self):
        if self.config_dic.get('LOG').get('log_level').upper() == 'DEBUG':
            import json
            self.log.debug(
                "start init:\n{}".format(json.dumps(self.config_dic, indent=4, sort_keys=False, ensure_ascii=False)))

    def get_log(self):
        return self.log

    def get_http(self, archive_id):
        return ConfigHttp(self.db.get_conn(), self.log, archive_id)

    def get_output_dir(self):
        return self.run_mode_config.get_output_dir()

    def get_db_conn(self):
        return self.db.get_conn()

    def get_run_mode(self):
        return self.run_mode_config.get_run_mode()

    def get_run_archive_id(self):
        return self.run_mode_config.get_run_archive_id()

    def get_run_case_list(self):
        return self.run_mode_config.get_case_list()

    def get_server_config(self):
        return (self.config_dic.get('SERVER').get('ipaddr'), int(self.config_dic.get('SERVER').get('listen_port')))

    def clear(self):
        self.db.get_conn().close()
        # self.db2.get_conn().close()



class Global:
    def __init__(self):
        self.log = configlog.config_log('../conf/global_config.ini', 'log_level')
        # self.dblog = configlog.config_log('../conf/global_config.ini', 'debug_db_log')
        #self.http = ConfigHttp('../conf/global_config.ini',self.log)
        self.db = GetDB('../conf/global_config.ini', 'DATABASE', self.log)
        #self.http = ConfigHttp(self.db1, self.log)
        self.run_mode_config = ConfigRunMode('../conf/global_config.ini')
    
    def get_log(self):
        return self.log

    def get_http(self, archive_id):
        return ConfigHttp(self.db.get_conn(), self.log, archive_id)

    def get_output_dir(self):
        return self.run_mode_config.get_output_dir()

    def get_db_conn(self):
        return self.db.get_conn()

    def get_run_mode(self):
        return self.run_mode_config.get_run_mode()

    def get_run_archive_id(self):
        return self.run_mode_config.get_run_archive_id()

    def get_run_case_list(self):
        return self.run_mode_config.get_case_list()

    def clear(self):
        self.db.get_conn().close()
        #self.db2.get_conn().close()

    # def get_dblog(self):
    #     return self.dblog


if __name__ == '__main__':
    GlobalConfig()
