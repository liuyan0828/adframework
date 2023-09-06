"""
-*- coding: utf-8 -*-
@Time : 2023/8/22 
@Author : liuyan
@function : 
"""
from libs.CompareXml import CompareXml
from libs.GetAdData import GetAdData
from Yaml.ReadYaml import read_yaml_file
import xml.etree.ElementTree as ET
import pytest
import os
from deepdiff import DeepDiff

# 获取当前项目所在路径
path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
filename = path_dir + r'/Yaml/xml_diff_case'
r = read_yaml_file(filename)


@pytest.mark.parametrize("data", r[0], ids=r[1])
def test_xml_diff(data):
    status = 0
    base_xml = CompareXml.get_root(path_dir + data['base_path'])
    base_el = CompareXml.get_all_elements(base_xml, status)
    res = GetAdData.get_ad_data(data['ad_url'])
    if res.status_code != 200:
        pytest.fail("接口请求失败:{}".format(res.status_code))
    else:
        if data['isEncrypt'] == 1:
            res_data = GetAdData.get_ad_decode_data(data['ad_url'])
        else:
            res_data = res.content.decode('utf-8')
        root = ET.XML(res_data)
        cur_el = CompareXml.get_all_elements(root, status)
        assert DeepDiff(base_el, cur_el) == {}