"""
-*- coding: utf-8 -*-
@Time : 2023/8/22 
@Author : liuyan
@function : 
"""
from libs.CompareXml import CompareXml
from libs.GetAdData import GetAdData
from utils.ReadYaml import read_yaml_files
from utils.RequestHandler import RequestHandler
import xml.etree.ElementTree as ET
import pytest
import os
from deepdiff import DeepDiff

# 获取当前项目所在路径
path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
r = read_yaml_files(path_dir + r'/Yaml/xml_diff_case')


# 重试的次数为3；可设置reruns=X
# 重试的间隔时间为1s；可设置reruns_delay=X
@pytest.mark.parametrize("data", r[0], ids=r[1])
@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_xml_diff(data):
    status = GetAdData.get_tvapi_data(data['ad_url'])
    base_xml = CompareXml.get_root(path_dir + data['base_path'])
    base_el = CompareXml.get_all_elements(base_xml, status)
    res = GetAdData.get_ad_data(data['ad_url'])
    if res.status_code != 200:
        pytest.fail("接口请求失败:{}".format(res.status_code))
    else:
        if data['isEncrypt'] == 1:
            res_data = RequestHandler.decode_xml_to_dict(res.content)
        else:
            res_data = res.content.decode('utf-8')
        root = ET.XML(res_data)
        cur_el = CompareXml.get_all_elements(root, status)
        assert DeepDiff(base_el, cur_el) == {}