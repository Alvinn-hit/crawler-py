# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 15:06:15 2017
@author: zhangxunan
crawl data from sina news
"""
import MySQLdb
def mysqlConnection(logger):
    try:
        conn = MySQLdb.connect(host='localhost',port = 3306,user='root', passwd='',db ='test',)
        conn.set_character_set('utf8')
        
        return conn
    except Exception as e:
        print e
        logger.exception("Exception Logged")
        return None

#�1�71�1�77�1�71�1�77�1�71�1�73�1�71�1�77�1�71�1�77�1�70�1�79
def mysqlSearch(conn, sqlSearch):
    cur = conn.cursor()
    try:
        cur.execute(sqlSearch)
        results = cur.fetchall()
        return results
    except Exception as e:
        print "Error: unable to fecth data"
        return e
def mysqlInsert(conn, sqlInsert,sqlValue):
    cur = conn.cursor()
    '''
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    '''
    try:
        cur.execute(sqlInsert,sqlValue)
        conn.commit()
        return 'Insert success'
    except Exception as e:
        conn.rollback()
        print (e)
        return e