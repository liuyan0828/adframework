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
from libs.Config import URL_CONFIG
from libs.GetAdConf import *


PATH = project_path + '/script'
case_dict = read_yaml_files(PATH)


@allure.feature("启动图")
class Test_Ad_Open():
    @pytest.fixture(autouse=True)
    def api_response(self, case_data):
        parameters = case_data['parameter']
        encoded_parameter = urllib.parse.urlencode(parameters)
        path = case_data['address']

        ad_url = path + "?" + encoded_parameter
        with allure.step("请求链接"):
            allure.attach(name="请求链接", body=str(URL_CONFIG['APP_AD_URL'] + ad_url))
        # 发送测试请求
        res = GetAdData.get_ad_data(ad_url)
        with allure.step("校验返回code"):
            allure.attach(name="期望code", body=str(200))
            allure.attach(name="实际code", body=str(res.status_code))
        assert res.status_code == 200
        for _ in range(20):
            res = GetAdData.get_ad_data(ad_url)
            res_data = json.loads(RequestHandler.decode_xml_to_dict(res.content).decode('utf-8'))
            if jsonpath.jsonpath(res_data, '$..lineid'):
                return res_data
        assert False, "返回数据为空"

    @allure.story("校验请求返回非空广告")
    @pytest.mark.parametrize("case_data", case_dict[0], ids=case_dict[1])
    def test_ad_res(self, case_data, api_response):
        allure.title(f"{case_data}")
        with allure.step("校验是否为空广告"):
            adtype = jsonpath.jsonpath(api_response, '$..adtype')[0]
        assert adtype != -1, "请检查投放，当前广告位返回的是空广告"

    @allure.story("校验广告基础配置是否同mango配置一致")
    @pytest.mark.parametrize("case_data", case_dict[0], ids=case_dict[1])
    def test_ad_config(self, case_data, api_response):
        """

        :param case_data: 测试用例
        :param api_response: 请求返回数据
        :return:
        """
        allure.title(f"{case_data}")
        payload = case_data['payload']
        mango_conf = GetAdConf(payload)
        template = mango_conf.get_adtemplate()
        res_template = jsonpath.jsonpath(api_response, '$..template')[0]
        with allure.step("校验返回template"):
            allure.attach(name="期望template", body=str(template))
            allure.attach(name="实际template", body=str(res_template))
        assert res_template == template
        if mango_conf.get_redirecttype() and mango_conf.get_redirecturl():
            redirecttype =  mango_conf.get_redirecttype()
            redirecturl = mango_conf.get_redirecturl()
            if redirecttype == "H5":
                res_redirecturl = jsonpath.jsonpath(api_response, '$..landing_url')[0]
                if res_redirecturl:
                    with allure.step("校验H5类型落地页"):
                        allure.attach(name="期望落地页", body=str(redirecturl))
                        allure.attach(name="实际落地页", body=str(res_redirecturl))
                    assert redirecturl == res_redirecturl
                else:
                    assert False, "mango配置了H5落地页但实际未下发"
        if mango_conf.get_clicktype():
            clicktype = mango_conf.get_clicktype()
            res_clicktype = jsonpath.jsonpath(api_response, '$..clicktype')[0]
            if res_clicktype:
                with allure.step("校验返回clicktype"):
                    allure.attach(name="期望clicktype", body=str(clicktype))
                    allure.attach(name="实际clicktype", body=str(res_clicktype))
                assert clicktype == res_clicktype
            else:
                assert False, "mango配置了clicktype但实际未下发"
        if mango_conf.get_isdeeplink():
            deeplinkflag = mango_conf.get_isdeeplink()
            res_deeplinkflag = jsonpath.jsonpath(api_response, '$..deeplinkflag')[0]
            if res_deeplinkflag:
                with allure.step("校验返回是否是deeplink"):
                    allure.attach(name="期望是否是deeplink", body=str(deeplinkflag))
                    allure.attach(name="实际是否是deeplink", body=str(res_deeplinkflag))
                assert deeplinkflag == res_deeplinkflag
            else:
                assert False, "mango配置了deeplinkflag但实际未下发"
        if mango_conf.get_buttontext():
            buttontext = mango_conf.get_buttontext()
            res_buttontext = jsonpath.jsonpath(api_response, '$..buttontxt.content')[0]
            if res_buttontext:
                with allure.step("校验返回按钮文案"):
                    allure.attach(name="期望按钮文案", body=str(buttontext))
                    allure.attach(name="实际按钮文案", body=str(res_buttontext))
                assert buttontext == res_buttontext
            else:
                assert False, "mango配置了按钮文案但实际未下发"

    @allure.story("校验请求返回：1、返回广告的排期包id是否为基准广告id 2、如果是对返回进行完全校验")
    @pytest.mark.parametrize("case_data", case_dict[0], ids=case_dict[1])
    def test_res_complete_check(self, case_data, api_response):
        allure.title(f"{case_data['title']}")
        expected_request = case_data['check']['expected_request']
        if isinstance(expected_request, str):
            _path = PATH + '/' + case_data['info']
            expected_request = read_json(case_data['info'], expected_request, _path)
        with allure.step("校验返回广告排期包id是否是基准配置广告排期包id"):
            lineid = jsonpath.jsonpath(api_response, '$..lineid')[0]
            expected_lineid = jsonpath.jsonpath(expected_request, '$..lineid')[0]
        assert lineid == expected_lineid, "当前广告位返回的lineid与基准配置的lineid不一致"
        with allure.step("校验返回data"):
            allure.attach(name="期望data", body=json.dumps(expected_request).encode('utf-8'), attachment_type=allure.attachment_type.JSON)
            allure.attach(name="实际data", body=json.dumps(api_response).encode('utf-8'), attachment_type=allure.attachment_type.JSON)
            expected_res = JsonHandle.get_target_result(expected_request)
            returned_res = JsonHandle.get_target_result(api_response)
        exclude_paths = {
            "root['impid']",  #每次不一样
            "root['ads'][0]['ad'][0]['creatives']['openvideo']['content']",  #加签
            "root['ads'][0]['ad'][0]['creatives']['video']['content']['sig']",  #加签
            "root['ads'][0]['ad'][0]['ext']['expiretime']",  #时间
            "root['ads'][0]['ad'][0]['deeplink_url']"  #deeplink_url不是http开头
        }
        diff_data = DeepDiff(expected_res, returned_res, ignore_order=True, exclude_paths=exclude_paths)
        allure.attach(name="diff", body=diff_data.to_json(), attachment_type=allure.attachment_type.JSON)
        print("diff_data:", diff_data.to_json())
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

