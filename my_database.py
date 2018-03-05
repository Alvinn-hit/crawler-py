#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/9/7 17:41
@Author  : typhoon
@Site    : 
@File    : my_database.py
@Software: PyCharm
@desc    :
"""

import configparser

import my_cx_oracle
import my_pymysql

config = configparser.ConfigParser()
config.read('conf.ini')
db_type = config['db']['type'] == 'mysql'


def get_conn():
    if db_type:
        conn = my_pymysql.get_conn()
    else:
        conn = my_cx_oracle.get_conn()
    return conn


def insert(conn, sql, param):
    if db_type:
        my_pymysql.insert(conn, sql, param)
    else:
        my_cx_oracle.insert(conn, sql, param)


def insert_model(conn, param):
    if db_type:
        my_pymysql.insert_model(conn, param)
    else:
        my_cx_oracle.insert_model(conn, param)

