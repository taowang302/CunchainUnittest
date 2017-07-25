import sys
sys.path.append("/root/unittest")
sys.path.append("/root/unittest/script")
from script.getdb import GetDB
from script.confighttp import ConfigHttp
import script.configlog as configlog
from script.runcase import RunCase
from script.htmlreport import HtmlReport
from script.configrunmode import ConfigRunMode
from configserver import ConfigServer
import datetime
import unittest
import json

class GlobalConfig:
    def __init__(self):
        self.log = configlog.config_log('../conf/global_config.ini')
        self.db = GetDB('../conf/global_config.ini', 'DATABASE', self.log)
        self.configserver = ConfigServer('../conf/global_config.ini')
    def get_log(self):
        return self.log

    def get_http(self, archive_id):
        return ConfigHttp(self.db.get_conn(), self.log, archive_id)

    def get_output_dir(self):
        return self.configserver.get_output()

    def get_http_config(self):
        return self.configserver.config_server()

    def get_db_conn(self):
        return self.db.get_conn()

    def clear(self):
        self.db.get_conn().close()


class Control:
    def __init__(self):
        self.global_config = GlobalConfig()

    def get_info(self):
        return_msg = {}
        try:
            db_conn = self.global_config.get_db_conn()
            db_cursor = db_conn.cursor()
            db_cursor.execute("SELECT file_number,description  FROM file_bag")
        except:
            err_reason = sys.exc_info()
            print("err_reason => {}\ntype => {}".format(err_reason,type(err_reason)))
            return {"status": "error", "data":'{}'.format(sys.exc_info()[1])}
        else:
            return_msg["status"] = "success"
            data = []
            file_bag = db_cursor.fetchall()
            total_nu = len(file_bag)
            return_msg["total_nu"] = total_nu
            for item in file_bag:
                db_cursor.execute("SELECT COUNT(case_number)  FROM usercase where from_view_id='{}'".format(item[0]))
                case_nu = db_cursor.fetchone()[0]
                data.append({"arhive_id":item[0],"case_nu":case_nu,"description":item[1]})
            return_msg["data"] = data
            return return_msg

    def run_case(self, archive_id):
        try:
            archive_id = ''.join(archive_id)
        except:
            return {"status":"error","data":"".format(sys.exc_info()[1])}
        start_time = datetime.datetime.now()
        db_conn = self.global_config.get_db_conn()
        log = self.global_config.get_log()
        http = ConfigHttp(db_conn, log, archive_id)
        runner = unittest.TextTestRunner()
        try:
            case_runner = RunCase()
            case_runner.run_case(runner, 1, [], db_conn, http, log, archive_id)
            end_time = datetime.datetime.now()
            output_dir = self.global_config.get_output_dir()
            html_report = HtmlReport(db_conn.cursor(), log, archive_id, 1, [])
            html_report.set_time_took(str(end_time - start_time))
            html_report.generate_html('test report', output_dir)
        except:
            return {"status":"error","data":"".format(sys.exc_info()[1])}
        else:
            case_total,success_nu,fail_nu,err_nu,report_url=html_report.get_info()
            self.global_config.clear()
            return{"status":"success","data":{"case_total":case_total,"success_nu":success_nu,"fail_nu":fail_nu,"err_nu":err_nu,"report_url":report_url}}

if __name__ == "__main__":
    pass
