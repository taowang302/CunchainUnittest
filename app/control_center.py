import sys
sys.path.append("/root/unittest")
sys.path.append("/root/unittest/script")
from script.getdb import GetDB
from script.confighttp import ConfigHttp
import script.configlog as configlog
from script.runcase import RunCase
from script.htmlreport import HtmlReport
from script.configrunmode import ConfigRunMode
import datetime
import unittest


class GlobalConfig:
    def __init__(self):
        self.log = configlog.config_log('../conf/global_config.ini')
        self.db = GetDB('../conf/global_config.ini', 'DATABASE', self.log)
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

    def get_run_case_list(self):
        return self.run_mode_config.get_case_list()

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
            return {"status": "error", "data":''.join(sys.exc_info()[1])}
        else:
            return_msg["status"] = "success"
            data = []
            file_bag = db_cursor.fetchall()
            for item in file_bag:
                db_cursor.execute("SELECT COUNT(case_number)  FROM usercase where from_view_id='{}'".format(item[0]))
                case_nu = db_cursor.fetchone()[0]
                data.append({"arhive_id":item[0],"case_nu":case_nu,"description":item[1]})
            return_msg["data"] = data
            return return_msg

    def run_case(self, archive_id):
        start_time = datetime.datetime.now()
        db_conn = self.global_config.get_db_conn()
        log = self.global_config.get_log()
        http = ConfigHttp(db_conn, log, archive_id)
        runner = unittest.TextTestRunner()
        case_runner = RunCase()
        case_runner.run_case(runner, 1, [], db_conn, http, log, archive_id)
        end_time = datetime.datetime.now()
        output_dir = self.global_config.get_output_dir()
        html_report = HtmlReport(db_conn.cursor(), log, archive_id, 1, [])
        html_report.set_time_took(str(end_time - start_time))
        html_report.generate_html('test report', output_dir)
        # global_config.clear()


if __name__ == "__main__":
    pass
