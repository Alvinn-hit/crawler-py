#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/25 16:23
@Author  : typhoon
@Site    : 
@File    : crawler_aviation.py
@Software: PyCharm
@desc    : 爬取《4、按月国内航线货邮运输量、国际航线货邮运输量》，解析PDF
"""
import random
import re
import time

from bs4 import BeautifulSoup

import my_cx_oracle
import my_database
import parse_pdf
import util_urllib
from my_log import logger


def parse_data(http_url, conn):
    # 获取网页
    resp = util_urllib.get_content_utf8(http_url)

    # 初始化bs4对象
    soup = BeautifulSoup(resp, "html.parser")

    # 过滤对象，找到标签a的href= r"\./.*/t.*\.html"，href='./201711/t20171120_47630.html'
    list_a = soup.find_all("a", href=re.compile(r'\./[\d]*/t[\d_]*\.html'))

    # 遍历a标签，访问下级页面
    for i, a in enumerate(list_a):
        if i > 2:
            # 取最近3月
            break
        # 获取a标签的文本，name='中国民航2017年9月份主要运输生产指标统计'
        name = a.get_text()

        # 解析文本中的日期，201709
        ym = re.sub(r'[^\d年\d]', "", name)
        if len(ym) == 6:
            ym = ym.replace('年', '-0')
        else:
            ym = ym.replace('年', '-')

        # 拼接下级页面地址：http://www.caac.gov.cn/XXGK/XXGK/TJSJ/201711/t20171120_47630.html
        http_url = "http://www.caac.gov.cn/XXGK/XXGK/TJSJ" + a['href'][1:]

        # 获取网页
        time.sleep(random.randint(1, 2))
        resp = util_urllib.get_content_utf8(http_url)

        # 初始化bs4对象
        soup = BeautifulSoup(resp, "html.parser")

        # 获取所需pdf地址的a标签。href= r"\./P\d*\.pdf"
        list_a = soup.find_all("a", href=re.compile(r"\./P\d*\.pdf"))

        # 拼接PDF页面地址
        date_str = a['href'][2:8]
        http_url = "http://www.caac.gov.cn/XXGK/XXGK/TJSJ/" + date_str + list_a[0]["href"][1:]

        # 解析PDF
        time.sleep(random.randint(1, 2))
        inland_volume, foreign_volume = parse_pdf.parse_pdf(http_url)

        # 国内航空货邮运输量
        insert(conn, 5, ym, inland_volume)
        # 国际航空货邮运输量
        insert(conn, 6, ym, foreign_volume)


def insert(conn, fid, month, value):
    # date
    hx_range = '国内航线'
    if fid == 6:
        hx_range = '国际航线'

    param = {
        "FID": fid,
        "MONTH": month,
        "RANGE": hx_range,
        "VALUE": value
    }
    try:
        my_database.insert_model(conn=conn, param=param)
    except Exception as e:
        if "PK" not in e:
            logger.exception("入库出错" + param)
            logger.error(e)


if __name__ == '__main__':
    url = "http://www.caac.gov.cn/XXGK/XXGK/TJSJ/index_1215.html"
    conn = my_cx_oracle.get_conn()
    parse_data(http_url=url, conn=conn)
