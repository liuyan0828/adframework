"""
-*- coding: utf-8 -*-
@Time : 2023/9/14 
@Author : liuyan
@function : 
"""
import allure
import pytest
import urllib.parse
from main import project_path
from utils.ReadYaml import read_yaml_file
from libs.GetAdData import *

PATH = project_path + '/script/' + "offer"

case_dict = read_yaml_file(PATH, "Template")


@allure.feature(case_dict["test_info"]["title"])
class TestTemplate:

    @pytest.mark.parametrize("case_data", case_dict["test_case"], ids=[])
    @allure.story("Template")
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_template(self, case_data):
        """

        :param case_data: 测试用例
        :return:
        """
        parameters = case_data['parameter']
        encoded_parameter = urllib.parse.urlencode(parameters)
        path = case_data['address']

        print(encoded_parameter)
        ad_url = path + "?" + encoded_parameter
        # 发送测试请求
        res_data = GetAdData.get_ad_data(ad_url)
        assert res_data.status_code == case_data['check']['expected_code']

