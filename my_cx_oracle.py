#!python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/25 15:06
@Author  : typhoon
@Site    :
@File    : my_cx_oracle.py
@Software: PyCharm
@desc    :
"""

import configparser
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import cx_Oracle

config = configparser.ConfigParser()
config.read('conf.ini')


def get_conn():
    # 获取数据库链接 jdbc:oracle:thin:@172.31.67.14:1521:default
    # conn=cx_Oracle.connect('ceaadmin/caeadmin@172.31.67.14/default')
    dsn = cx_Oracle.makedsn(config['db']['host'], config['db']['port'], config['db']['dbname'])
    conn = cx_Oracle.connect(
        config['db']['user'],
        config['db']['pass'],
        dsn
    )
    return conn


def insert_model(conn, param):
    """

    :param conn:
    :param param: {'MONTH':'2017-01','VALUE':3}
    :return:
    """

    sql = "insert into T_TS_IMPACT_FACTOR_HIS(FID,IMPACT_RANGE,YM,VALUE,UPDATER) " \
          " values(:FID,:RANGE,:MONTH,:VALUE,'crawler')"
    if check_fk(conn=conn, param=param):
        insert(conn, sql, param)


def check_fk(conn, param):
    if param["VALUE"] == 0:
        return False
    cursor = conn.cursor()
    sql = "select * from  T_TS_IMPACT_FACTOR_HIS where fid=" + str(param["FID"]) + " and ym= '" + str(
        param["MONTH"]) + "'"
    cursor.execute(sql)
    row = cursor.fetchall()
    for x in row:
        return False
    return True


from my_log import logger


def insert(conn, sql, param):
    """
    :param conn: conn
    :param sql: sql
    :param param
    """
    # 获取会话指针
    cursor = conn.cursor()
    # 执行sql语句
    cursor.execute(sql, param)
    conn.commit()
    logger.info("insert:" + str(param))


if __name__ == '__main__':
    con = get_conn()
    print(con)

    params = {"FID": "1000", "MONTH": "2017-01", "VALUE": 3}
    # check_FK(conn=con, param=params)
    insert_model(conn=con, param=params)
    con.commit()
    print("end")
