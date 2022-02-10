"""
-*- coding: utf-8 -*-
@Time : 2021/12/13 
@Author : liuyan
@function : 前置处理
"""
import os

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def preprocess(request):
    print("fixture部分-path:{}".format(request.param['base_path']))
    print("fixture部分-url:{}".format(request.param['ad_url']))
    print("fixture部分-isEncrypt:{}".format(request.param['isEncrypt']))
    return request.param


def pytest_collection_modifyitems(items):
    """
    测试用例搜集完成时，将搜集到的 item 的 name 和 nodeid的中文显示在控制台上
    :param items:
    :return:
    """
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode_escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode_escape')





