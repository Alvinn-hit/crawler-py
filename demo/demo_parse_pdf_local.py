#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/17 18:07
@Author  : typhoon
@Site    :
@File    : test_has_package_python3.py
@Software: PyCharm
@desc:
"""

import importlib
import sys

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument

'''
 解析pdf 文本，保存到txt文件中
'''
importlib.reload(sys)


def parse(_path):
    fp = open(_path, 'rb')  # rb以二进制读模式打开

    # 用文件对象来创建一个pdf文档分析器
    praser_pdf = PDFParser(fp)

    # 创建一个PDF文档
    doc = PDFDocument()

    # 连接分析器 与文档对象
    praser_pdf.set_document(doc)
    doc.set_parser(praser_pdf)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()

        # 创建一个PDF参数分析器
        laparams = LAParams()

        # 创建聚合器
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # 创建一个PDF页面解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一页的内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            # 使用页面解释器来读取
            interpreter.process_page(page)

            # 使用聚合器获取内容
            layout = device.get_result()

            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for out in layout:
                # 判断是否含有get_text()方法，图片之类的就没有
                # if hasattr(out,"get_text"):
                if isinstance(out, LTTextBoxHorizontal):

                    results = out.get_text()
                    # print("results: " + results)
                    with open(r'pdf_val.txt', 'a') as f:
                        if "运输完成情况" in results:
                            target_value = results.split("\n")
                            inland_amount = target_value[10]
                            foreign_amount = target_value[12]
                            print("国内货邮运输量：", inland_amount, "国际货邮运输量：", foreign_amount)
                            f.write("国内货邮运输量:" + inland_amount + ",国际货邮运输量:" + foreign_amount + "\n")
                            f.close()
                            break


if __name__ == '__main__':
    path = r'G:\项目\4、东航客机腹舱买断收入预测系统\爬虫\PDF爬取模块-数据示例.pdf'
    parse(path)
