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

    @allure.story("校验xml是否能返回：1、校验返回ad是否与基准一致 2、完全校验")
    @pytest.mark.flaky(reruns=10, reruns_delay=1)
    @pytest.mark.parametrize("case_data", case_dict[0], ids=case_dict[1])
    def test_ad_xml(self, case_data):
        allure.title(f"{case_data['title']}")
        # prot=vast则返回xml
        case_data['parameter']['prot'] = 'vast'
        res = check_code(case_data)
        res_data = RequestHandler.decode_xml_to_dict(res.content)
        assert res_data != {}
        # xml存放路径
        path = PATH + '/' + case_data['info'] + '/' + case_data['check']['expected_xml']
        base_xml = CompareXml.get_root(path)
        expected_request = CompareXml.get_all_elements(base_xml)
        root = ET.XML(res_data)
        api_response = CompareXml.get_all_elements(root)
        check_xml_res(api_response, expected_request)
