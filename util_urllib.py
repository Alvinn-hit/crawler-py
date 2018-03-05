#! python3 
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/29 15:38
@Author  : typhoon
@Site    : 
@File    : util_urllib.py
@Software: PyCharm
@desc    :
"""
import configparser
import json
import random
import time
from urllib import parse
from urllib import request

from my_log import logger

user_agents = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
    'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

config = configparser.ConfigParser()
config.read('conf.ini')
reconnection_count = int(config['timer']['reconnection_count'])
time_out = int(config['timer']['url_time_out'])

# proxy_handler = request.ProxyHandler({'http': '172.31.1.246:8080'})
# opener = request.build_opener(proxy_handler)
# request.install_opener(opener)


def get_content_utf8(request_url):
    html = get_resp(request_url)
    if html == "":
        return ""
    else:
        content = html.read().decode("utf-8")
        return content


def get_json_utf8(http_url):
    return json.loads(get_content_utf8(http_url))


def get_resp(request_url):
    """
    模拟浏览器拉取数据
    :param request_url:地址
    :return: str
    """

    req = request.Request(request_url)
    req.add_header("user_agent", random.choice(user_agents))

    return urlopen(req)


def post_resp(request_url, post_data, headers):
    """

    :param request_url:
    :param post_data: [("key","value")]
    :param headers: {"key":"value"}  "User-Agent"已经有了其他特殊的可用此参数
    :return:
    """
    req = request.Request(request_url)
    for header in headers:
        req.add_header(header, headers[header])
    data = parse.urlencode(post_data).encode("utf-8")
    req.add_header("User-Agent", random.choice(user_agents))

    return urlopen(req, data)


def post_content_utf8(request_url, post_data, headers):
    resp = post_resp(request_url, post_data, headers)
    status = resp.status
    html = resp.read().decode("utf-8")
    return status, html


def post_json_utf8(request_url, post_data, headers):
    return json.loads(post_content_utf8(request_url, post_data, headers))


def urlopen(url, data=""):
    # 出错重连，默认3次
    for i in range(reconnection_count):
        try:
            if data == "":
                resp = request.urlopen(url=url, timeout=time_out)
            else:
                resp = request.urlopen(url=url, data=data, timeout=time_out)
            logger.info("获取" + url.full_url + "内容成功")
            return resp
        except Exception as e:
            logger.error(e)
            logger.error("第" + str(i + 1) + "次请求失败：" + url.full_url)
            time.sleep(3)
    return ""


if __name__ == '__main__':
    ''' # 1
    	数据爬虫访问网址如下：
		中国民航局 http://www.caac.gov.cn/XXGK/XXGK/TJSJ/index_1215.html
		WTI原油价格：https://cn.investing.com/commodities/crude-oil-historical-data
		国家统计局：http://data.stats.gov.cn/easyquery.htm?cn=A01
    '''
    # 2 网页地址 实际地址在conf.ini
    # con = get_content_utf8('http://www.caac.gov.cn/XXGK/XXGK/TJSJ/index_1215.html')
    # con = get_content_utf8('http://data.stats.gov.cn/easyquery.htm?cn=A01')
    # con = get_content_utf8('https://cn.investing.com/commodities/crude-oil-historical-data')
