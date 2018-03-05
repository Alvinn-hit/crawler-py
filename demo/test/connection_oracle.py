#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/9/4 17:55
@Author  : typhoon
@Site    : 
@File    : connection_oracle.py
@Software: PyCharm
@desc    :
"""

import cx_Oracle
# conn=cx_Oracle.connect('cea/ceaadmin@9.186.56.223/default')
dsn = cx_Oracle.makedsn("9.186.56.223", "1521", "default")
conn = cx_Oracle.connect("cea", "ceaadmin", dsn)

cursor = conn.cursor()
sql = "Insert into TEST_DEMO_USER (ID,NAME,AGE,BIRTHDAY) values (2,'ytf',18,to_date('2005-09-17','yyyy-mm-dd'))"
cursor.execute(sql)
conn.commit()


#连接数据库
c=conn.cursor()                                           #获取cursor
x=c.execute('select sysdate from dual')                   #使用cursor进行各种操作
x.fetchone()
c.close()                                                 #关闭cursor
conn.close()                                              #关闭连接