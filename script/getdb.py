#!/usr/bin/env python
# -*- coding:utf-8 -*-


import configparser
import mysql.connector
import sys

class GetDB:
    '''配置数据库IP，端口等信息，获取数据库连接'''

    def __init__(self, dbconfig, log, sql_log=None):
        self.log = log
        # 从配置文件中读取数据库服务器IP、域名，端口
        self.host = dbconfig.get('host')
        self.port = dbconfig.get('port')
        self.user = dbconfig.get('user')
        self.passwd = dbconfig.get('passwd')
        self.db = dbconfig.get('db')
        self.charset = dbconfig.get('charset')
        self.conn = self.get_conn()
        self.db_log = sql_log

    def get_conn(self):
        try:
            conn = mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.passwd, database=self.db, charset=self.charset)
            return conn
        except Exception as e:
            self.log.error(e)
            sys.exit()

    def run_sql(self, sql):
        self.db_log.debug(sql)
        db_cursor = self.conn.cursor()
        db_cursor.execute(sql)
        return db_cursor


if __name__ == "__main__":
    import configlog

    dblog = configlog.config_db_log({
        "log_level": "debug",
        "debug_db_log": "true",
        "log_path": "../log/unittest.log",
        "console_log": 'true'
    })
    log = configlog.config_log({
        "log_level": "debug",
        "debug_db_log": "true",
        "log_path": "../log/unittest.log",
        "console_log": 'true'})
    db = GetDB({
        "host": "192.168.168.137",
        "port": "3306",
        "user": "root",
        "passwd": "jbi123456",
        "db": "unittest",
        "charset": "utf8"
    }, log, dblog)

    db_cursor = db.run_sql("SELECT COUNT(file_number)  FROM file_bag where file_number='f_001'")
    log.info(db_cursor.fetchone()[0])
