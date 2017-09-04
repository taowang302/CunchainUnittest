import sys
#sys.path.append("/root/unittest")
#sys.path.append("/root/unittest/script")

sys.path.append('/'.join(sys.path[0].split('/')[:-1]))
sys.path.append("{}/script".format('/'.join(sys.path[0].split('/')[:-1])))
# from script.getdb import GetDB
from script.confighttp import ConfigHttp
# import script.configlog as configlog
from script.runcase import RunCase
from script.htmlreport import HtmlReport
# from configserver import ConfigServer
import datetime
import unittest
from globalconfig import GlobalConfig


# class GlobalConfig:
#     def __init__(self):
#         self.log = configlog.config_log('../conf/global_config.ini', 'log_level')
#         self.db = GetDB('../conf/global_config.ini', 'DATABASE', self.log)
#         self.configserver = ConfigServer('../conf/global_config.ini')
#     def get_log(self):
#         return self.log
#
#     def get_http(self, archive_id):
#         return ConfigHttp(self.db.get_conn(), self.log, archive_id)
#
#     def get_output_dir(self):
#         return self.configserver.get_output()
#
#     def get_http_config(self):
#         return self.configserver.config_server()
#
#     def get_db_conn(self):
#         return self.db.get_conn()
#
#     def clear(self):
#         self.db.get_conn().close()


class Control:
    def __init__(self):
        self.global_config = GlobalConfig()
        self.db_conn = self.global_config.get_db_conn()
        self.db_cursor = self.db_conn.cursor()
        self.log = self.global_config.get_log()

    def get_server_config(self):
        return self.global_config.get_server_config()

    def get_info(self):
        return_msg = {}
        try:
            self.db_cursor.execute("SELECT file_number,description  FROM file_bag")
        except:
            return {"status": "error", "data":'{}'.format(sys.exc_info()[1])}
        else:
            return_msg["status"] = "success"
            data = []
            file_bag = self.db_cursor.fetchall()
            total_nu = len(file_bag)
            return_msg["total_nu"] = total_nu
            for item in file_bag:
                self.db_cursor.execute(
                    "SELECT COUNT(case_number)  FROM usercase where from_view_id='{}'".format(item[0]))
                case_nu = self.db_cursor.fetchone()[0]
                data.append({"arhive_id":item[0],"case_nu":case_nu,"description":item[1]})
            return_msg["data"] = data
            return return_msg
    
    def get_case_info(self,archive_id):
        try:
            archive_id = ''.join(archive_id)
        except:
            return {"status":"error","data":"".format(sys.exc_info()[1])}
        try:
            self.db_cursor.execute("SELECT file_number FROM file_bag")
        except:
            return {"status": "error", "data":'{}'.format(sys.exc_info()[1])}
        else:
            archive_id_list = self.db_cursor.fetchall()
            if ('{}'.format(archive_id),) not in archive_id_list:
                return {"status": "error", "data":'Invalid Archive ID'}
        try:
            self.db_cursor.execute("SELECT case_number,case_name,http_method,description  FROM usercase where from_view_id='{}'".format(archive_id))
        except:
            return {"status": "error", "data":'{}'.format(sys.exc_info()[1])}
        else:
            archive_info = self.db_cursor.fetchall()
            return_msg ={}
            data = []
            for item in archive_info:
                data.append({"case id":item[0],"api":item[1],"method":item[2],"description":item[3]})
            return {"status":"success","total":len(archive_info),"data":data}

    def run_case(self, archive_id):
        try:
            archive_id = ''.join(archive_id)
        except:
            return {"status":"error","data":"".format(sys.exc_info()[1])}
        start_time = datetime.datetime.now()
        db_conn = self.global_config.get_db_conn()
        log = self.global_config.get_log()
        try:
            http = ConfigHttp(db_conn, log, archive_id)
        except ValueError as e:
            return {"status":"error","data":"{}".format(e)}
        except:
            return {"status":"error","data":"{}".format(sys.exc_info()[1])}
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
            return {"status":"error","data":"{}".format(sys.exc_info()[1])}
        else:
            case_total,success_nu,fail_nu,err_nu,report_url=html_report.get_info()
            self.global_config.clear()
            return{"status":"success","data":{"case_total":case_total,"success_nu":success_nu,"fail_nu":fail_nu,"err_nu":err_nu,"report_url":report_url}}

if __name__ == "__main__":
    pass
