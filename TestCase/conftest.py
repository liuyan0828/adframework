"""
-*- coding: utf-8 -*-
@updateTime : 2022/06/14
@Author : liuyan
@function : 前置处理+优化断言报错
"""
import os
import sys
import TestCase

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


# def pytest_assertrepr_compare(op, left, right):
#     if op == '==':
#         return[
#             f"返回存在多余字段"
#         ]






