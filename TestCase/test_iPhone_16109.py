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
from main import project_path
from utils.ReadYaml import read_yaml_file
from libs.GetAdData import *
from utils.checkResult import check_result
from utils.RequestHandler import RequestHandler

PATH = project_path + '/script/' + "iPhone_16109"

case_dict = read_yaml_file(PATH, "iPhone_16109")


@allure.feature(case_dict["test_info"]["title"])
class TestIphone16109:

    @pytest.mark.parametrize("case_data", case_dict["test_case"], ids=[])
    @allure.story("iPhone_16109")
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_iphone_16109(self, case_data):
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
        res_data = RequestHandler.decode_xml_to_dict(res.content)
        assert res.status_code == case_data['check']['expected_code']
        if isinstance(case_data['check'], list):
            for i in case_data['check']:
                check_result(case_data["test_name"], i, res_data[1].status_code, res_data.json(), PATH)
        else:
            check_result(case_data["test_name"], case_data['check'], res.status_code, json.loads(res_data.decode()), PATH)


