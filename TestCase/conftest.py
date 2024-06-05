"""
-*- coding: utf-8 -*-
@updateTime : 2022/06/14
@Author : liuyan
@function : 前置处理+优化断言报错
"""
import os
import sys
import pytest
import json
from libs.GetAdData import *
from libs.checkResult import check_code

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture()
def api_response(case_data):
    """
    :param case_data: yaml文件读取的case
    :function: 前置操作用于获取接口返回；test函数中有api_response参数即使用此fixture
    """
    res = check_code(case_data)
    try:
        res_data = json.loads(RequestHandler.decode_xml_to_dict(res.content).decode('utf-8'))
    except Exception as e:
        res_data = json.loads(res.content)
    return res_data


def pytest_collection_modifyitems(items):
    """
    测试用例搜集完成时，将搜集到的 item 的 name 和 nodeid的中文显示在控制台上
    :param items:
    :return:
    """
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode_escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode_escape')








