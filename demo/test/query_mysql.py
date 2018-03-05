#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/24 17:18
@Author  : typhoon
@Site    : 
@File    : query_mysql.py
@Software: PyCharm
@desc    :
"""
import pymysql.cursors

# 查询数据库
# 获取数据库链接
connection = pymysql.connect(host="localhost",
                             user="root",
                             password="passw0rd",
                             db="csdn_blog",
                             charset="utf8mb4")
try:
    # 获取会话指针
    with connection.cursor() as cursor:
        # 创建sql语句
        sql = "select `url`,`blog_title` from `myblog` where `digg_count` is null"
        # 执行sql语句
        count = cursor.execute(sql)
        print(count)
        # result = cursor.fetchall()
        result = cursor.fetchmany(size=2)
        print(result)


finally:
    connection.close();
