from globalconfig import Global
from getdb import GetDB

global_config = Global()

log = global_config.get_log()
dblog = global_config.get_dblog()

db = GetDB('../conf/global_config.ini', 'DATABASE', log, dblog)

db.run_sql("SELECT count(case_number) FROM test_result where from_view_id='f_001')
