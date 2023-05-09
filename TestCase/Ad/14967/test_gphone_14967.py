"""
-*- coding: utf-8 -*-
@Time : 2021/12/13
@Author : liuyan
@function : gphone启动图广告测试用例
"""
import json

from libs.CompareXml import CompareXml
from libs.GetAdData import GetAdData
from Yaml.ReadYaml import ReadYaml
import xml.etree.ElementTree as ET
import pytest
import os
from deepdiff import DeepDiff

# 获取当前项目所在路径
path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
filename = path_dir + r'/Yaml/14967/gphone搜索结果页'
r = ReadYaml(filename).GetTestData()


@pytest.mark.parametrize("data", r[0], ids=r[1])
@pytest.mark.flaky(reruns=4)
def test_diff(data):
    status=0
    base_xml = CompareXml.get_root(path_dir + data['base_path'])
    base_el = CompareXml.get_all_elements(base_xml,status)
    if data['isEncrypt'] == 1:
        res = GetAdData.get_ad_decode_data(data['ad_url'])
    else:
        res = GetAdData.get_ad_data(data['ad_url'])
    root = ET.XML(res)
    cur_el = CompareXml.get_all_elements(root, status)
    assert  DeepDiff(base_el, cur_el) == {}
