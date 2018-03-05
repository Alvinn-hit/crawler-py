#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/25 15:06
@Author  : typhoon
@Site    : 
@File    : pymysql.py
@Software: PyCharm
@desc    :
"""

import configparser

import pymysql.cursors

config = configparser.ConfigParser()
config.read('conf.ini')


def get_conn():
    # 获取数据库链接
    conn = pymysql.connect(host=config['db']['host'],
                           user=config['db']['user'],
                           db=config['db']['dbname'],
                           password=config['db']['pass'],
                           charset=config['db']['charset'])
    return conn


def insert(conn, sql, param):
    # 获取会话指针
    with conn.cursor() as cursor:
        # 执行sql语句
        cursor.execute(sql, param)
        conn.commit()


def insert_model(conn, param):
    """

    :param conn:
    :param param: {第几行|指标类型ID，指标名称，日期：年月，年，月，值，数据类型}
    """
    params = []
    for v in param.values():
        params.append(v)

    sql = "Insert into ORIGINAL_DATA (NAME_INDEX,NAME,DATA_DATE,YEAR,MONTH,VALUE,UNIT,DATA_TYPE,CREATE_TIME) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,now())"
    insert(conn, sql, params)

