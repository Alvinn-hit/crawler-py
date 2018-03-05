#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/25 13:27
@Author  : typhoon
@Site    : 
@File    : crawler.py
@Software: PyCharm
@desc    :
"""

import calendar
import datetime
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import my_pymysql


def get_html_content(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "id('data_interval')"))).click()
        time.sleep(0.5)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "id('flatDatePickerCanvasHol')"))).click()
        time.sleep(0.5)
        start_date = driver.find_element_by_id("startDate")
        end_date = driver.find_element_by_id("endDate")
        start_date.clear()
        end_date.clear()
        # 获取上月的日期字符串 as 2017/07/01  2017/07/31
        last_month_start, last_month_end = get_last_month()
        start_date.send_keys(last_month_start)
        end_date.send_keys(last_month_end)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "id('applyBtn')"))).click()
        time.sleep(3)

        return BeautifulSoup(driver.page_source, "html.parser"), last_month_start[:7]
    except Exception as e:
        print(e)
        return None


def get_data(date_str, soup4=BeautifulSoup("", "html.parser"), data_type=5):
    # print(soup4)
    table = soup4.find(id="placehereresult2")
    # print(table)
    tds = table.find_all("td")
    # print(tds)
    for td in tds:
        # print(td)
        str = td.get_text()
        if "平均" in str:
            val = td.span.get_text()
            print("平均值", val)
            _date_time = datetime.datetime.strptime(date_str, '%Y/%m')
            insert(1, "WTI原油期货", _date_time, int(date_str[:4]), int(date_str[5:7]), val, data_type)
            break


def insert(index, name, date, year, month, value, data_type):
    sql = "insert into `original_data`(`index`,`name`,`date`,`year`,`month`,`value`,`data_type`,`create_time`) values(%s,%s,%s,%s,%s,%s,%s,now())"
    # param = (第几行|指标类型ID，指标名称，日期：年月，年，月，值，数据类型)
    param = (index, name, date, year, month, value, data_type)
    my_pymysql.insert(conn, sql, param)


def get_last_month():
    """
    return str:start, str:end
    """
    end_time = (datetime.date.today().replace(day=1) - datetime.timedelta(1))
    start_time = end_time.replace(day=1)
    start = start_time.strftime('%Y/%m/%d')
    end = end_time.strftime('%Y/%m/%d')
    return start, end


def get_month_first_day_and_last_day(year=None, month=None):
    """
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    :return: first_day: 当月的第一天，datetime.date类型
              last_day: 当月的最后一天，datetime.date类型
    """
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    first_day_week_day, month_range = calendar.monthrange(year, month)

    # 获取当月的第一天
    first_day = datetime.date(year=year, month=month, day=1)
    last_day = datetime.date(year=year, month=month, day=month_range)

    return first_day, last_day


if __name__ == '__main__':

    # 获取数据库链接
    conn = my_pymysql.get_conn()
    try:
        browser = webdriver.Firefox(executable_path=r'E:\develop\python-driver\geckodriver.exe')
        url = "https://cn.investing.com/commodities/crude-oil-historical-data"
        browser.get(url)
        soup, datestr = get_html_content(browser)
        browser.quit()

        # last_month_start, last_month_end = get_last_month()
        # datestr = last_month_start[0:7]
        # file = r"C:\Users\yuan\Desktop\开发\aaa.txt"
        # text = open(file, "r", encoding="utf-8").read()
        # soup = BeautifulSoup(text, "html.parser")

        get_data(soup4=soup, date_str=datestr)

        # get_last_month()
    finally:
        conn.close()
        print("end")
