#!/usr/bin/env python
# -*- coding:utf-8 -*-
import configparser

class ConfigRunMode:
    def __init__(self, run_case_config_file):
        config = configparser.ConfigParser()

        # 从配置文件中读取运行模式
        config.read(run_case_config_file)
        try:
            self.run_mode = config['RUNCASECONFIG']['runmode']
            self.run_mode = int(self.run_mode)
            self.case_list = config['RUNCASECONFIG']['case_id']
            self.case_list = eval(self.case_list)  # 把字符串类型的list转换为list
            self.output_dir = config['OUTPUT']['output_dir']
            self.archive_id = config['RUNCASECONFIG']['archive_id']
        except Exception as e:
            print('%s', e)

    def get_run_mode(self):
        return self.run_mode
    
    def get_run_archive_id(self):
        return self.archive_id

    def get_case_list(self):
        return  self.case_list
    
    def get_output_dir(self):
        return self.output_dir
