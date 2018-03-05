#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/17 17:41
@Author  : typhoon
@Site    : 
@File    : parse_pdf.py
@Software: PyCharm
@desc    : 解析在线PDF
"""

import random
from io import StringIO
import util_urllib
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf

from my_log import logger

user_agent = ['Mozilla/5.0 (Windows NT 10.0; WOW64)', 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
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
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']


def read_pdf(pdf_file):
    rsrc_mgr = PDFResourceManager()
    ret_str = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrc_mgr, ret_str, laparams=laparams)

    process_pdf(rsrc_mgr, device, pdf_file)
    device.close()

    content = ret_str.getvalue()
    ret_str.close()
    return content


def parse_pdf(http_url):
    pdf_file = util_urllib.get_resp(http_url)
    output_string = read_pdf(pdf_file)
    pdf_file.close()

    output_string = output_string.replace(" ", "")
    target_value = output_string.split("\n")
    for obj in target_value:
        if obj == "":
            target_value.remove(obj)
    # 运输完成情况的序号
    value_index = 0
    # 运输总周转量的序号
    total_turnover = 0
    # 货邮运输量的序号
    goods_transport_volume = 0
    # 第一个数字的序号
    num_index = 0
    for i, val in enumerate(target_value):
        # print(val)
        if "运输总周转量" in val:
            total_turnover = i
            continue
        if "货邮运输量" in val:
            goods_transport_volume = i
            continue
        if "运输完成情况" in val:
            value_index = i
            continue
        if total_turnover > 10 and "." in val:
            num_index = i
            break
    if total_turnover > 10:
        # print((goods_transport_volume - total_turnover) / 2)
        # print(int((goods_transport_volume - total_turnover) / 2) + 2)
        # print(int((goods_transport_volume - total_turnover) / 2) + 4)
        inland_volume = target_value[num_index + int((goods_transport_volume - total_turnover) / 2) + 1]
        foreign_volume = target_value[num_index + int((goods_transport_volume - total_turnover) / 2) + 3]
    else:
        inland_volume = target_value[value_index + goods_transport_volume - total_turnover + 2]
        foreign_volume = target_value[value_index + goods_transport_volume - total_turnover + 4]

    # print("total_turnover:", total_turnover, "goods_transport_volume:", goods_transport_volume, "value_index",
    #       value_index, "num_index:", num_index)
    # print("国内货邮运输量：", inland_volume, "国际货邮运输量：", foreign_volume)
    logger.info("国内货邮运输量：%s 国际货邮运输量：%s" % (inland_volume, foreign_volume))
    return float(inland_volume), float(foreign_volume)


if __name__ == '__main__':
    # print(random.randint(5, 10) * 0.2)
    url = "http://www.caac.gov.cn/XXGK/XXGK/TJSJ/201707/P020170720576685272748.pdf"
    url = "http://www.caac.gov.cn/XXGK/XXGK/TJSJ/201602/P020160224588701073792.pdf"
    url = "http://www.caac.gov.cn/XXGK/XXGK/TJSJ/201609/P020160920365608824975.pdf"
    url = "http://www.caac.gov.cn/XXGK/XXGK/TJSJ/201706/P020170620373231069735.pdf"
    print( parse_pdf(url))

