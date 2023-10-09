"""
-*- coding: utf-8 -*-
@Time : 2023/9/13 
@Author : liuyan
@function : 
"""

import logging
import time
import sys
from utils.MakeDir import mk_dir


class LogConfig:
    def __init__(self, path):
        """
        :param path: 路径
        """
        runtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        mk_dir(path, "/log")
        logfile = path + "/log/" + runtime + ".log"
        logfile_err = path + "/log/" + runtime + "_err.log"

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.handlers = []

        # 创建一个handler，用于写入全部info日志文件
        fh = logging.FileHandler(logfile, mode="a+")
        fh.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入全部error日志文件
        fh_err = logging.FileHandler(logfile_err, mode="a+")
        fh_err.setLevel(logging.ERROR)

        # 创建一个handler，用于输出到控制台
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        fh_err.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 将logger添加handler
        logger.addHandler(fh)
        logger.addHandler(fh_err)
        logger.addHandler(ch)
