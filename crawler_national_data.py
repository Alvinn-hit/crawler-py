#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/24 16:49
@Author  : typhoon
@Site    : 
@File    : test.py
@Software: PyCharm
@desc    :爬取国家统计数据
1、按月社会消费品零售总额_当期值：
2、按月进口总值_当期值、按月出口总值_当期值
3、民航货运量_当期值
"""
import datetime
import time

import my_database
import util_urllib
from my_log import logger


def parse_json(data, data_type, conn):
    """
    解析json对象，并入库
    :param conn: mysql连接对象
    :param data_type: 数据类型
    :param data:json对象
    :return: 200 OK,其他 ERROR
    """

    # 校验请求是否正常
    status = data["returncode"]
    if status != 200:
        # return null, "error"
        logger.error("error status:" + status)
        return status

    returndata = data["returndata"]
    # 为记录中文，遍历并初始化names {code:name}
    wdnodes = returndata["wdnodes"]
    names = {}
    units = {}
    for wdnode in wdnodes:
        nodes = wdnode["nodes"]
        if wdnode["wdcode"] == "zb":
            for node in nodes:
                code = node["code"]
                names[code] = node["cname"]
                units[code] = node["unit"]

    # 遍历并插入数据库
    datanodes = returndata["datanodes"]
    index = 0
    index_code = ""
    for i, datanode in enumerate(datanodes):
        data_val = datanode["data"]["data"]
        zb_code = ""
        sj_code = ""
        for wds in datanode["wds"]:
            if wds["wdcode"] == "zb":
                zb_code = wds["valuecode"]
            if wds["wdcode"] == "sj":
                sj_code = wds["valuecode"]
        name = names[zb_code]
        unit = units[zb_code]
        date = time.strptime(sj_code, "%Y%m")
        data_date = datetime.datetime.strptime(sj_code, "%Y%m").date()
        if index_code != zb_code:
            index = index + 1
            index_code = zb_code
        yearmonth = sj_code[0:4] + "-" + sj_code[4:6]

        if '社会消费品零售总额_当期值' in name:
            insert(conn, 1, yearmonth, int(data_val))
        if '进口总值_当期值' == name:
            insert(conn, 2, yearmonth, int(data_val))
        if '出口总值_当期值' == name:
            insert(conn, 3, yearmonth, int(data_val))
        if '民航货运量_当期值' in name:
            insert(conn, 4, yearmonth, int(data_val))

    return 200


def insert(conn, fid, month, value):
    # date
    param = {
        "FID": fid,
        "MONTH": month,
        "RANGE":"全部航线",
        "VALUE": value
    }
    try:
        my_database.insert_model(conn=conn, param=param)
    except Exception as e:
        if "PK" not in e:
            logger.exception("入库出错" + param)
            logger.error(e)


"""
def insert(conn, index, name, data_date, year, month, value, unit, data_type):
    # date
    param = {
        "NAME_INDEX": index,
        "NAME": name,
        "DATA_DATE": data_date,
        "YEAR": year,
        "MONTH": month,
        "VALUE": value,
        "UNIT": unit,
        "DATA_TYPE": data_type
    }
    my_database.insert_model(conn=conn, param=param)
"""


def parse_data(url, date_type, conn):
    logger.info("请求地址：" + url)
    json_data = util_urllib.get_json_utf8(url)
    status = parse_json(json_data, date_type, conn)
    if status != 200:
        logger.error("请求地址：" + url)


'''
if __name__ == '__main__':
    logger.info("MOVE!")
    # 获取数据库链接
    conn = my_pymysql.get_conn()
    try:
        # 最近13个月的值（不含当月）
        # 1、按月社会消费品零售总额_当期值
        http_url = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgyd&rowcode=zb&colcode=sj&wds=[]&dfwds=[{"wdcode":"zb","valuecode":"A1501"}]&k1=1502953145649'
        json1 = util_urllib.get_json_content(http_url)
        logger.info(parse_json(json1, 1) + http_url)
        time.sleep(random.randint(2, 5))

        # 2、按月进口总值_当期值、按月出口总值_当期值
        http_url = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgyd&rowcode=zb&colcode=sj&wds=[]&dfwds=[{"wdcode":"zb","valuecode":"A1601"}]&k1=1502954973845'
        json2 = util_urllib.get_json_content(http_url)
        logger.info(parse_json(json2, 2) + http_url)
        time.sleep(random.randint(2, 5))

        # 3、民航货运量_当期值
        http_url = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgyd&rowcode=zb&colcode=sj&wds=[]&dfwds=[{"wdcode":"zb","valuecode":"A1701"}]&k1=1502954973845'
        json3 = util_urllib.get_json_content(http_url)
        logger.info(parse_json(json3, 3) + http_url)
    finally:
        conn.close()
        logger.info("OVER!")
'''
