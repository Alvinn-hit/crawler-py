#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/30 10:35
@Author  : typhoon
@Site    : 
@File    : job.py
@Software: PyCharm
@desc    :
"""
import configparser
import random
import time

import crawler_aviation
import crawler_crude_prices
import crawler_national_data
import my_database
from my_log import logger

config = configparser.ConfigParser()
config.read('conf.ini')

url_national_data1 = config['address']['url_national_data1']
data_type_national_data1 = config['address']['data_type_national_data1']

url_national_data2 = config['address']['url_national_data2']
data_type_national_data2 = config['address']['data_type_national_data2']

url_national_data3 = config['address']['url_national_data3']
data_type_national_data3 = config['address']['data_type_national_data3']

url_aviation = config['address']['url_aviation']
data_type_aviation = config['address']['data_type_aviation']

url_crude_prices = config['address']['url_crude_prices']
data_type_crude_prices = config['address']['data_type_crude_prices']


def task():
    logger.info("---收集数据开始---")
    if "2" == "2":
        start_time = time.time()
        # 获取mysql连接
        try:
            conn = my_database.get_conn()

            '''
            try:
                logger.info("1、收集国家统计数据-“按月社会消费品零售总额_当期值”开始")
                start_time2 = time.time()
                crawler_national_data.parse_data(url_national_data1, data_type_national_data1, conn)
                conn.commit()
                end_time = time.time()
                logger.info("1、收集国家统计数据-“按月社会消费品零售总额_当期值”完毕 用时：%.3fs" % (end_time - start_time2))
                time.sleep(random.randint(3, 7))
            except Exception as e:
                logger.error(e)
            '''

            try:
                logger.info("2、收集国家统计数据-“按月进口总值_当期值、按月出口总值_当期值”开始")
                start_time3 = time.time()
                crawler_national_data.parse_data(url_national_data2, data_type_national_data2, conn)
                conn.commit()
                end_time = time.time()
                logger.info("2、收集国家统计数据-“按月进口总值_当期值、按月出口总值_当期值”完毕 用时：%.3fs" % (end_time - start_time3))
                time.sleep(random.randint(3, 7))
            except Exception as e:
                logger.error(e)
            '''
            try:
                logger.info("3、收集国家统计数据-“民航货运量_当期值”开始")
                start_time4 = time.time()
                crawler_national_data.parse_data(url_national_data3, data_type_national_data3, conn)
                conn.commit()
                end_time = time.time()
                logger.info("3、收集国家统计数据-“民航货运量_当期值”完毕 用时：%.3fs" % (end_time - start_time4))
            except Exception as e:
                logger.error(e)
            '''
            try:
                logger.info("4、收集货邮数据“按月国内航线货邮运输量、国际航线货邮运输量”开始")
                start_time5 = time.time()
                crawler_aviation.parse_data(url_aviation, conn)
                conn.commit()
                end_time = time.time()
                logger.info("4、收集货邮数据“按月国内航线货邮运输量、国际航线货邮运输量”完毕 用时：%.3fs" % (end_time - start_time5))
            except Exception as e:
                logger.error(e)

            try:
                logger.info("5、收集“WTI原油价格”开始")
                start_time6 = time.time()
                crawler_crude_prices.parse_data(url_crude_prices, conn)
                conn.commit()
                end_time = time.time()
                logger.info("5、收集“WTI原油价格”完毕 用时：%.3fs" % (end_time - start_time6))
            except Exception as e:
                logger.error(e)

            result = "---收集数据完毕--- 用时：%.3fs"
        except Exception as e:
            logger.exception("")
            logger.error(e)
            result = "---收集数据异常--- 用时：%.3fs"
            conn.rollback()
        finally:
            conn.close()
            end_time = time.time()
            used_time = end_time - start_time
            logger.info(result % used_time)


def start():
    year = config["task"]["year"]
    month = config["task"]["month"]
    day = config["task"]["day"]
    hour = config["task"]["hour"]
    minute = config["task"]["min"]

    is_time_do_something = True
    while True:
        now = time.localtime()
        is_now_year = year == "" or now[0] == int(year)
        is_now_month = month == "" or now[1] == int(month)
        is_now_day = day == "" or now[2] == int(day)
        is_now_hour = hour == "" or now[3] == int(hour)
        is_now_min = minute == "" or now[4] == int(minute)

        is_now = is_now_year and is_now_month and is_now_day and is_now_hour and is_now_min
        '''
            当达到指定日期时执行一次，执行完等待下一次日期
            
            以每月2日执行（day=1,其他为空，不填）为例：今天是1日
            is_now为false不会执行，则等待。
            明天（2日）：is_now为true，此时因为之前一直执行else内容所以is_time_do_something必然为true
            则可执行task，当此次task执行完毕之后is_time_do_something设置为false，然后因为今天是2日
            所以is_now一直为true，并不会改变is_time_do_something的值，换句话说2日这天只能执行1次任务，
            然后就等待下一个2日
        '''
        if is_now:
            if is_time_do_something:
                # task()
                _thread.start_new_thread(task, ())
                print('run-------------------------run-------------------------run-------------------------')
            is_time_do_something = False
        else:
            is_time_do_something = True
        print(time.strftime("%Y-%m-%d %H:%M:%S", now))
        time.sleep(10)


import _thread

if __name__ == '__main__':
    # _thread.start_new_thread(start, ())
    # while True:
    #     time.sleep(60)
    start()
