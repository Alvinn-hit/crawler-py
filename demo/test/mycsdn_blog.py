#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/24 16:11
@Author  : typhoon
@Site    : 
@File    : mycsdn_blog.py
@Software: PyCharm
@desc    :
"""

from bs4 import BeautifulSoup
from urllib import request
import re
import pymysql.cursors

url = "http://blog.csdn.net/y515789"

# 打开网站
resp = request.urlopen(url)

# 使用BeautifulSoup解析网站
soup = BeautifulSoup(resp.read().decode("utf-8"), "html.parser")

# 获取所有以href=XXXX开头的a标签
list_titles = soup.find_all("a", href=re.compile("^/y515789/article/details/"))
# 输出所有的文章标题以及地址
for title in list_titles:
    href = "http://blog.csdn.net" + title["href"]
    text = title.get_text().replace("\n","").strip()
    # 过滤评论和阅读a标签
    if not re.search("(阅读|评论)",text):
        blog = request.urlopen(href)
        soup = BeautifulSoup(blog.read().decode("utf-8"), "html.parser")
        digg = soup.find(id="btnDigg").dd
        bury = soup.find(id="btnBury").dd
        print(text, "--->", href, digg.get_text(), bury.get_text())

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
                sql = "insert into `myblog`(`blog_title`,`url`,`digg_count`,`bury_count`) values(%s,%s,%s,%s)"
                # 执行sql语句
                cursor.execute(sql, (text, href, digg.get_text(), bury.get_text()))
                connection.commit();
        finally:
            connection.close();