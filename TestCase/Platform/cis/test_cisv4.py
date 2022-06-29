"""
-*- coding: utf-8 -*-
@Time : 2022/5/7 
@Author : liuyan
@function : 
"""

import allure
import json
from libs.RequestHandler import RequestHandler
from deepdiff import DeepDiff
from Yaml.ReadYaml import ReadYaml
import pytest
import os

# 获取当前项目所在路径
path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
filename = path_dir + r'/Yaml/Platform/cisv4'
r = ReadYaml(filename).GetTestData()


@pytest.mark.parametrize("data", r[0], ids=r[1])
@allure.feature('Cis')
def test_cis_01(data):
    request = RequestHandler()
    res1 = request.request_main('post', data['base_url'], json=data['paramater'])
    res2 = request.request_main('post', data['url'], json=data['paramater'])
    assert not DeepDiff(json.loads(res1.text), json.loads(res2.text))