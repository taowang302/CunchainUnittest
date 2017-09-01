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
        # self.dblog = sql_log
        # self.log.debug(
        # "db config:\nhost => {}\nport => {}\nuser => {}\npasswd =>{} \ndb => {}\ncharset => {}".format(self.host,
        #                                                                                                self.port,
        #                                                                                                self.user,
        #                                                                                                self.passwd,
        #                                                                                                self.db,
        #                                                                                                self.charset))
        # if sql_log:
        #     self.conn = self.get_conn()
        #     self.cursor = self.conn.cursor()

    def get_conn(self):
        try:
            conn = mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.passwd, database=self.db, charset=self.charset)
            return conn
        except Exception as e:
            self.log.error(e)
            sys.exit()

            # def run_sql(self, sql):
            #     self.dblog.debug(sql)
            #     try:
            #         return self.cursor.execute(sql)
            #     except:
            #         self.log.error(sys.exc_info()[1])
            #         return
