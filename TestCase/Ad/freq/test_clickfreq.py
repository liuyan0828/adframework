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
import requests
import time
from urllib.parse import urlparse

# 获取当前项目所在路径
path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
filename = path_dir + r'/Yaml/freq/clickfreq'
r = ReadYaml(filename).GetTestData()
print(r)
@pytest.mark.parametrize("data", r[0], ids=r[1])
def test_diff(data):
    for i in range(0, 3):
        res = GetAdData.get_ad_data(data['ad_url'])
        root = ET.XML(res)
        url = root[0][0][5][0][0][2][2].text
        a = requests.get(url)
        time.sleep(3)
    res = GetAdData.get_ad_data(data['ad_url'])
    root = ET.XML(res)
    text= root[0][0][4].text
    assert DeepDiff(text, None) == {}









