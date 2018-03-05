#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/25 13:27
@Author  : typhoon
@Site    : 
@File    : crawler.py
@Software: PyCharm
@desc    : 爬取《5、WTI原油价格》
注意：headers = {"X-Requested-With": "XMLHttpRequest"}
"""

import calendar
import datetime

from bs4 import BeautifulSoup

import my_database
import util_urllib
from my_log import logger


def get_html_content(http_url):
    """
    获取网页对象
    :param http_url:地址
    :return: BeautifulSoup对象，日期字符串 as 2017/07/01
    """
    try:
        # 获取上月的日期字符串 as 2017/07/01  2017/07/31
        last_month_start, last_month_end = get_last_month()
        post_data = [
            ("curr_id", "8849"),
            ("smlID", "300060"),
            ("st_date", last_month_start),
            ("end_date", last_month_end),
            ("interval_sec", "Daily"),
            ("sort_col", "date"),
            ("sort_ord", "DESC"),
            ("action", "historical_data")
        ]
        headers = {"X-Requested-With": "XMLHttpRequest"}

        status, html = util_urllib.post_content_utf8(http_url, post_data, headers)

        # print(status, html)
        if 200 == status:
            return BeautifulSoup(html, "html.parser"), last_month_start
        else:
            logger.warn("status:" + status)
    except Exception as e:
        logger.error(e)
        return None, ""
    logger.error("status:" + status + " url:" + http_url)
    return None, ""


def get_data(conn, date_str, soup4, data_type=5):
    # print(soup4)
    table = soup4.find(id="placehereresult2")
    # print(table)
    tds = table.find_all("td")
    # print(tds)
    for td in tds:
        # print(td)
        text = td.get_text()
        if "平均" in text:
            val = td.span.get_text()
            logger.info("平均值" + val + date_str)
            # 2017/02/03
            yearmonth = date_str[0:4] + "-" + date_str[5:7]
            # 原油价格
            insert(conn, 7, yearmonth, float(val))
            break


def insert(conn, fid, month, value):
    # date
    param = {
        "FID": fid,
        "MONTH": month,
        "RANGE": "全部航线",
        "VALUE": value
    }
    try:
        my_database.insert_model(conn=conn, param=param)
    except Exception as e:
        if "PK" not in e:
            logger.exception("入库出错" + param)
            logger.error(e)


"""
def insert(conn, index, name, data_date, year, month, value, data_type):
    # date
    param = {
        "NAME_INDEX": index,
        "NAME": name,
        "DATA_DATE": data_date,
        "YEAR": year,
        "MONTH": month,
        "VALUE": float(value),
        "UNIT": "",
        "DATA_TYPE": data_type
    }
    my_database.insert_model(conn=conn, param=param)
"""


# 获取上月第一天日期和最后一天日期
def get_last_month():
    """
    return str:start, str:end
    """
    end_time = (datetime.date.today().replace(day=1) - datetime.timedelta(1))
    start_time = end_time.replace(day=1)
    start = start_time.strftime('%Y/%m/%d')
    end = end_time.strftime('%Y/%m/%d')
    return start, end

# 获取某年某月的第一天日期和最后一天日期
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


def parse_data(http_url, conn):
    logger.info("请求url:" + http_url)
    soup, date_str = get_html_content(http_url)

    if soup is not None:
        get_data(conn=conn, date_str=date_str, soup4=soup)
    else:
        logger.error("获取数据失败，请检查网络连接")


'''
if __name__ == '__main__':
    # 获取数据库链接
    conn = my_pymysql.get_conn()
    # 获取数据库链接
    http_url = "https://cn.investing.com/instruments/HistoricalDataAjax"
    parse_data(http_url, conn)
'''
if __name__ == '__main__':
    print(get_last_month())
