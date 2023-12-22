"""
-*- coding: utf-8 -*-
@Time : 2023/9/14 
@Author : liuyan
@function : 
"""
import allure
import pytest
import urllib.parse
import json
import jsonpath
from deepdiff import DeepDiff
from main import project_path
from utils.ReadYaml import read_yaml_files
from utils.readExpectedResult import read_json
from libs.GetAdData import *
from libs.CompareXml import *


PATH = project_path + '/script'
case_dict = read_yaml_files(PATH)


class TestJsonDiff:

    @pytest.mark.parametrize("case_data", case_dict[0], ids=case_dict[1])
    @allure.story("{ids}")
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_json_diff(self, case_data):
        """

        :param case_data: 测试用例
        :return:
        """
        parameters = case_data['parameter']
        encoded_parameter = urllib.parse.urlencode(parameters)
        path = case_data['address']

        ad_url = path + "?" + encoded_parameter
        # 发送测试请求
        res = GetAdData.get_ad_data(ad_url)
        res_data = json.loads(RequestHandler.decode_xml_to_dict(res.content).decode('utf-8'))
        # print(res_data)
        expected_request = case_data['check']['expected_request']
        if isinstance(expected_request, str):
            _path = PATH + '/' + case_data['info']
            expected_request = read_json(case_data['info'], expected_request, _path)
        with allure.step("校验返回code"):
            allure.attach(name="期望code", body=str(case_data['check']["expected_code"]))
            allure.attach(name="实际code", body=str(res.status_code))
        assert res.status_code == case_data['check']['expected_code']
        with allure.step("校验是否为空广告"):
            adtype = jsonpath.jsonpath(res_data, '$..adtype')[0]
        assert adtype != -1, "请检查投放，当前广告位返回的是空广告"
        with allure.step("校验返回广告是否是基准配置广告"):
            lineid = jsonpath.jsonpath(res_data, '$..lineid')[0]
            expected_lineid = jsonpath.jsonpath(expected_request, '$..lineid')[0]
        assert lineid == expected_lineid, "当前广告位返回的lineid与基准配置的lineid不一致"
        with allure.step("校验返回data"):
            allure.attach(name="期望data", body=str(expected_request))
            allure.attach(name="实际data", body=str(res_data))
            expected_res = JsonHandle.get_target_result(expected_request)
            returned_res = JsonHandle.get_target_result(res_data)
        exclude_paths = {
            "root['impid']",
            "root['ads'][0]['ad'][0]['creatives']['openvideo']['content']",
            "root['ads'][0]['ad'][0]['ext']['expiretime']"
        }
        diff_data = DeepDiff(expected_res, returned_res, ignore_order=True, exclude_paths=exclude_paths)
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

