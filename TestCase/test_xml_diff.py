"""
-*- coding: utf-8 -*-
@Time : 2023/8/22 
@Author : liuyan
@function : 
"""
import xml.etree.ElementTree as ET
import pytest
import os
import allure
from libs.CompareXml import CompareXml
from libs.GetAdData import GetAdData
from utils.ReadYaml import read_yaml_files
from utils.RequestHandler import RequestHandler
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
        with allure.step("校验返回data"):
            allure.attach(name="期望data", body=str(base_el))
            allure.attach(name="实际data", body=str(cur_el))
        exclude_paths = {
            "root['impid']",
            "root['ads'][0]['ad'][0]['creatives']['openvideo']['content']",
            "root['ads'][0]['ad'][0]['ext']['expiretime']"
        }
        diff_data = DeepDiff(base_el, cur_el, ignore_order=True, exclude_paths=exclude_paths)
        allure.attach(name="diff", body=str(diff_data))
        # print(diff_data.to_json())
        if diff_data == {}:
            assert True, "校验通过"
        elif "dictionary_item_added" in diff_data:
            assert False, "返回数据中存在新增字段"
        elif "dictionary_item_removed" in diff_data:
            assert False, "返回数据中缺少部分字段"
        elif "values_changed" in diff_data:
            assert False, "返回数据中部分字段的值与基准不一致"
        elif "type_changes" in diff_data:
            assert False, "返回数据中部分字段类型与基准不一致"
        elif "iterable_item_added" in diff_data:
            assert False, "返回数据中存在新增列表项"
        elif "iterable_item_removed" in diff_data:
            assert False, "返回数据中缺少部分列表项"
        else:
            assert False, "返回数据与基准不一致"