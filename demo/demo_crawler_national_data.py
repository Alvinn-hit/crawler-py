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

import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import my_pymysql

# 获取数据库链接
conn = my_pymysql.get_conn()

global browser


def get_html_content(urlStr, id1, id2):
    global browser
    # browser = webdriver.Chrome()
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "id('" + id1 + "')"))).click()
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "id('" + id2 + "')"))).click()
        soup = BeautifulSoup(browser.page_source, "html.parser")
        return soup
    except Exception as e:
        print(e)
        return None


def get_data(soup=BeautifulSoup("", "html.parser"), data_type=1):
    table = soup.find_all("table", class_="public_table table_fix")[0]
    ths = table.thead.tr.find_all("th")
    data_tr = table.tbody.find_all("tr")
    for j, tr in enumerate(data_tr):
        tds = tr.find_all("td")
        zb = "指标"
        name = "社会消费品零售总额_同比增长(%)"
        for i, td in enumerate(tds):
            if i == 0:
                zb = ""
                name = td.get_text()
                continue
            date = ths[i].get_text()
            val = td.get_text()
            if val == "":
                val = 0
            t = time.strptime(date, "%Y年%m月")
            print(j, name, date, val)
            insert(j, name, t, int(t[0]), int(t[1]), float(val), data_type)


def insert(index, name, date, year, month, value, data_type):
    sql = "insert into `original_data`(`index`,`name`,`date`,`year`,`month`,`value`,`data_type`,`create_time`) values(%s,%s,%s,%s,%s,%s,%s,now())"
    # param = (第几行|指标类型ID，指标名称，日期：年月，年，月，值，数据类型)
    param = (index, name, date, year, month, value, data_type)
    my_pymysql.insert(conn, sql, param)


try:
    browser = webdriver.Firefox(executable_path=r'F:\develop\python-driver\geckodriver.exe')
    browser.maximize_window()
    url = "http://data.stats.gov.cn/easyquery.htm?cn=A01"
    browser.get(url)

    soup = get_html_content(url, "treeZhiBiao_7_span", "treeZhiBiao_14_span")
    time.sleep(1)
    soup2 = get_html_content(url, "treeZhiBiao_8_span", "treeZhiBiao_19_span")
    time.sleep(1)
    soup3 = get_html_content(url, "treeZhiBiao_9_span", "treeZhiBiao_21_span")

    url = "http://www.caac.gov.cn/XXGK/XXGK/TJSJ/index_1215.html"
    browser.get(url)

    browser.quit()

    get_data(soup, 1)
    get_data(soup2, 2)
    get_data(soup3, 3)
finally:
    conn.close()


# file = r"C:\Users\IBM_ADMIN\Desktop\demo\python-爬虫\soup.txt"
# text = open(file, "r", encoding="utf-8").read()
# soup = BeautifulSoup(text, "html.parser")
