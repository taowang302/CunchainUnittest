#!/usr/bin/env python
# -*- coding:utf-8 -*-

class ConfigRunMode:
    def __init__(self, run_case_config):
        try:
            self.run_mode = int(run_case_config.get('runmode'))
            self.case_list = eval(run_case_config.get('case_id'))
            # self.case_list = eval(self.case_list)  # 把字符串类型的list转换为list
            self.output_dir = run_case_config.get('output_dir')
            self.archive_id = run_case_config.get('archive_id')
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
