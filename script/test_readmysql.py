import MySQLdb

conn = MySQLdb.connect(host="localhost",port = 3306,user="root",passwd="jbi123456",db ="webdemo")
cur = conn.cursor()
data_nu = cur.execute("select * from unittest")