#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/8/30 15:50
@Author  : typhoon
@Site    : 
@File    : my_log.py
@Software: PyCharm
@desc    :
https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
https://docs.python.org/3.6/library/logging.html
"""

import configparser
import logging
import os
from logging import handlers

config = configparser.ConfigParser()
config.read('./conf.ini')
log_level = config["log"]["log_level"]
log_name = config["log"]["log_name"]


class Logger:
    if __name__ == '__main__':
        logger_name = 'ef.log'

        name = logger_name.split('/')
        file_name = name[len(name) - 1]
        if len(name) != 1:
            n = len(file_name)
            file_dir = logger_name[:len(logger_name) - n - 1]

            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
                print(1, file_dir)
        if not os.path.exists(logger_name):
            print(2, file_name)
            fp = open(logger_name, 'w')
            fp.close()

    def __init__(self, logger_name=log_name):

        name = logger_name.split('/')
        file_name = name[len(name) - 1]
        if len(name) != 1:
            n = len(file_name)
            file_dir = logger_name[:len(logger_name) - n - 1]
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
        if not os.path.exists(logger_name):
            fp = open(logger_name, 'w')
            fp.close()

        level = int(log_level)
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)

        log_suffix = config["log"]["log_suffix"]
        when = config["log"]["when"]
        interval = int(config["log"]["interval"])
        # 所有日志输出的文件（level设定级别）
        fh = handlers.TimedRotatingFileHandler(filename=logger_name, when=when, interval=interval, encoding="utf-8")
        fh.suffix = log_suffix
        fh.setLevel(level)

        # 错误日志输出的文件
        handler_error = handlers.TimedRotatingFileHandler(
            filename=logger_name.split('.')[0] + "_error." + logger_name.split('.')[1], when=when, interval=interval,
            encoding="utf-8")
        handler_error.suffix = log_suffix
        handler_error.setLevel(logging.ERROR)

        # 创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(level)

        error_log_format = config["log"]["error_log_format"]
        info_log_format = config["log"]["info_log_format"]
        info_log_format = "\n\n" + info_log_format.replace("\\n", "\n")
        error_log_format = "-" * 80 + "\n" + error_log_format.replace("\\n", "\n")

        fh.setFormatter(logging.Formatter(info_log_format))
        handler_error.setFormatter(logging.Formatter(error_log_format))
        ch.setFormatter(logging.Formatter(error_log_format))
        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(handler_error)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger


logger = Logger().getlog()
'''
if __name__ == "__main__":
    # logging初始化工作
    logging.basicConfig()
    # nor的初始化工作
    nor = logging.getLogger("nor")
    nor.setLevel(logging.INFO)
    # 定义一个1分钟换一次log文件的handler
    filehandler = logging.handlers.TimedRotatingFileHandler(
        "logs/logging_test", 'H', 1, 0)
    # 设置后缀名称，跟strftime的格式一样
    filehandler.suffix = "%Y%m%d-%H%M.log"
    nor.addHandler(filehandler)
    nor.info("start..")
    while True:
        time.sleep(2)
        nor.info(time.ctime())
'''
if __name__ == '__main__':
    logger.info("[2017-12-19 12:03:41,935] INFO in util_urllib:113: 获取http://www.caac.gov.cn/XXGK/XXGK/TJSJ/201709/P020170920425214729354.pdf内容成功")