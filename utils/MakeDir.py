"""
-*- coding: utf-8 -*-
@Time : 2023/9/13 
@Author : liuyan
@function : 
"""
import os
import logging
import re


def mk_dir(path):
    # 去除首位空格
    path = path.strip()
    path = path.rstrip("\\")
    path = path.rstrip("/")

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            logging.error("创建文件夹失败，请检查路径是否正确，错误信息为：{}".format(e))
    else:
        logging.debug("文件夹{}已存在，无需创建".format(path))
        pass
