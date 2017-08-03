import configlog
import configdblog

# db = GetDB('../conf/global_config.ini', 'DATABASE', log, dblog)

log = configlog.config_log('../conf/global_config.ini', 'log_level')
log.info("test")
dblog = configdblog.config_db_log('../conf/global_config.ini')
dblog.debug("test")
