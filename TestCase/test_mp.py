"""
-*- coding: utf-8 -*-
@Time : 2023/9/14
@Author : liuyan
@function :
"""
import pytest
from main import project_path
from utils.ReadYaml import read_yaml_files
from utils.readExpectedResult import *
from libs.GetAdConf import *
from libs.checkResult import *


PATH = project_path + '/script/mp'
case_dict = read_yaml_files(PATH)


@allure.feature("通栏")
class Test_Ad_Mp():
    @allure.story("1、校验非空广告 2、校验返回的lineid与ad 3、完全校验")
    # 重试10次间隔1s；3次中只要有一次成功case即成功
    @pytest.mark.flaky(reruns=10, reruns_delay=1)
    @pytest.mark.parametrize("case_data", case_dict[0], ids=case_dict[1])
    def test_ad_config(self, case_data, api_response):
        """

        :param case_data: 测试用例
        :param api_response: 请求返回数据
        :function: 校验mango配置是否一致
        """
        allure.title(f"{case_data}")
        check_adtype(api_response)
        expected_request = case_data['check']['expected_request']
        if isinstance(expected_request, str):
            _path = PATH + '/' + case_data['info']
            expected_request = read_json(case_data['info'], expected_request, _path)
        check_lineid(api_response, expected_request)
        check_returned_data(api_response, expected_request)

