"""
-*- coding: utf-8 -*-
@Time : 2023/9/25 
@Author : liuyan
@function : 
"""
import json
import urllib
import allure
import jsonpath
from deepdiff import DeepDiff
from libs.GetAdData import GetAdData
from libs.CompareXml import JsonHandle, CompareXml
from libs.Config import URL_CONFIG
from utils.RequestHandler import RequestHandler
from utils.UrlHandler import *
import xml.etree.ElementTree as ET


def check_json(src_data, dst_data):
    if isinstance(src_data, dict):
        for key in src_data:
            if key not in dst_data:
                raise Exception("Json格式校验，关键字{}不在返回结果中".format(key))
            else:
                this_key = key
                if isinstance(src_data[this_key], dict) and isinstance(dst_data[this_key], dict):
                    check_json(src_data[this_key], dst_data[this_key])
                elif isinstance(type(src_data[this_key]), type(dst_data[this_key])):
                    raise Exception("Json格式校验，关键字{}与{}的类型与预期不符".format(src_data[this_key], dst_data[this_key]))
                else:
                    pass
    else:
        raise Exception("Json格式校验，返回结果格式错误")


def check_and_assert(get_value, api_response, response_path, assert_msg, error_msg):
    """
    :param get_value: 获取对应配置项函数
    :param api_response: 接口返回数据
    :param response_path: 接口返回配置的jsonpath路径
    :param assert_msg: assert失败报错文案
    :param error_msg: 未获取配置时报错文案
    """
    value = get_value()
    if value:
        res_value = jsonpath.jsonpath(api_response, response_path)
        if res_value:
            with allure.step(f"校验返回{get_value.__name__}"):
                allure.attach(name=f"期望{get_value.__name__}", body=str(value))
                allure.attach(name=f"实际{get_value.__name__}", body=str(res_value[0]))
            assert value == res_value[0], assert_msg
        else:
            assert False, error_msg


def check_adtype(api_response):
    """
    :param api_response: 接口返回数据
    """
    with allure.step("校验是否为空广告；adtype为-1：空广告；0：常规广告；1：可跳过广告"):
        # adtype = -1：空广告；0：常规广告；1：可跳过广告
        adtype = jsonpath.jsonpath(api_response, '$..adtype')[0]
        allure.attach(name="adtype", body=str(adtype))
    assert adtype != -1, "请检查投放，当前广告位返回的是空广告"


def check_lineid(api_response, expected_request):
    """
    :param api_response: 接口返回数据
    :param expected_request: 预期返回数据（基准）
    :return:
    """
    with allure.step("校验返回广告排期包id是否是基准配置广告排期包id"):
        lineid = jsonpath.jsonpath(api_response, '$..lineid')[0]
        expected_lineid = jsonpath.jsonpath(expected_request, '$..lineid')[0]
        allure.attach(name="实际lineid", body=str(lineid))
        allure.attach(name="期望lineid", body=str(expected_lineid))
    assert lineid == expected_lineid, "当前广告位返回的lineid与基准配置的lineid不一致"


def check_redirect(mango_conf, api_response):
    """
    :param mango_conf: 获取mango配置返回
    :param api_response: 接口返回数据
    :return:
    """
    redirecttype = mango_conf.get_redirecttype()
    redirecturl = mango_conf.get_redirecturl()
    appletId = mango_conf.get_appletId()
    if redirecttype and (redirecturl or appletId):
        # 落地页配置类型为H5时，接口返回url的key才为landing_url；后续待补充其他类型
        if redirecttype == "H5":
            res_redirecturl = jsonpath.jsonpath(api_response, '$..landing_url')[0]
            if res_redirecturl:
                with allure.step("校验H5类型落地页"):
                    allure.attach(name="期望落地页", body=str(redirecturl))
                    allure.attach(name="实际落地页", body=str(res_redirecturl))
                assert redirecturl == res_redirecturl, '返回的H5落地页url与配置不一致'
            else:
                assert False, "mango配置了H5落地页但实际未下发"
        elif redirecttype == "deeplink":
            res_redirecturl = jsonpath.jsonpath(api_response, '$..deeplink_url')[0]
            if res_redirecturl:
                with allure.step("校验deeplink类型落地页"):
                    allure.attach(name="期望落地页", body=str(redirecturl))
                    allure.attach(name="实际落地页", body=str(res_redirecturl))
                assert redirecturl == res_redirecturl, '返回的deeplink落地页url与配置不一致'
            else:
                assert False, "mango配置了deeplink落地页但实际未下发"
        elif redirecttype == "wechat_applet":
            res_redirecturl = jsonpath.jsonpath(api_response, '$..mini_click_through')[0]
            res_appletId =  jsonpath.jsonpath(api_response, '$..mini_id')[0]
            if res_appletId:
                with allure.step("校验微信小程序id"):
                    allure.attach(name="期望微信小程序id", body=str(appletId))
                    allure.attach(name="实际微信小程序id", body=str(res_appletId))
                assert appletId == res_appletId, '返回的微信小程序id与配置不一致'
            else:
                assert False, "mango配置了微信小程序id但实际未下发"
            if redirecturl:
                if res_redirecturl:
                    with allure.step("校验微信小程序落地页"):
                        allure.attach(name="期望微信小程序落地页", body=str(redirecturl))
                        allure.attach(name="实际微信小程序落地页", body=str(res_redirecturl))
                    assert redirecturl == res_redirecturl, '返回的微信小程序落地页url与配置不一致'
                else:
                    assert False, "mango配置了微信小程序落地页但实际未下发"


def check_code(case_data):
    """
    校验code
    :param parameter: 请求参数
    :param api_response: 接口返回数据
    :return: 接口返回
    """
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
    return res


def check_diff(diff_data):
    """
    :param diff_data: deepdiff返回的差异数据
    :function: 优化assert输出
    """
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


def check_returned_data(api_response, expected_request):
    """
    :param api_response: 接口返回数据
    :param expected_request: 基准配置返回数据
    :return:
    """
    # 获取广告id，即url中的ad值；如为空广告则不会走到这一步
    exp_ad = UrlHandler(expected_request['ads'][0]['ad'][0]['event_monitor'][0]['url']).get_value('ad')
    res_ad = UrlHandler(api_response['ads'][0]['ad'][0]['event_monitor'][0]['url']).get_value('ad')
    with allure.step("校验返回广告ID"):
        allure.attach(name="期望广告ID", body=str(exp_ad))
        allure.attach(name="实际广告ID", body=str(res_ad))
    assert exp_ad == res_ad, "当前广告位返回的广告ID与基准配置的广告ID不一致"
    with allure.step("校验返回data"):
        allure.attach(name="期望data", body=json.dumps(expected_request).encode('utf-8'),
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(name="实际data", body=json.dumps(api_response).encode('utf-8'),
                      attachment_type=allure.attachment_type.JSON)
        expected_res = JsonHandle.get_target_result(expected_request)
        returned_res = JsonHandle.get_target_result(api_response)
    # 排除路径：不进行diff对比
    exclude_paths = {
        "root['impid']",  #每次不一样
        "root['ads'][0]['ad'][0]['creatives']['openvideo']['content']",  #加签
        "root['ads'][0]['ad'][0]['creatives']['video']['content']['sig']",  #加签
        "root['ads'][0]['ad'][0]['ext']['expiretime']",  #时间
        "root['ads'][0]['ad'][0]['deeplink_url']"  #deeplink_url不是http开头
    }
    diff_data = DeepDiff(expected_res, returned_res, ignore_order=True, exclude_paths=exclude_paths)
    allure.attach(name="diff", body=diff_data.to_json(), attachment_type=allure.attachment_type.JSON)
    check_diff(diff_data)


def check_xml_res(api_response, expected_request):
    # 获取广告id，即url中的ad值；
    exp_ad = UrlHandler(expected_request['Impression'][0]['text']).get_value('ad')
    res_ad = UrlHandler(api_response['Impression'][0]['text']).get_value('ad')
    if res_ad == "该url中无对应key，请检查输入":
        assert False, "请检查投放，当前广告位返回的是空广告"
    with allure.step("校验返回广告ID"):
        allure.attach(name="期望广告ID", body=str(exp_ad))
        allure.attach(name="实际返回", body=json.dumps(expected_request), attachment_type=allure.attachment_type.JSON)
        allure.attach(name="实际广告ID", body=str(res_ad))
    assert exp_ad == res_ad, "当前广告位返回的广告ID与基准配置的广告ID不一致"
    exclude_paths = {
        "root['impid']",
        "root['ads'][0]['ad'][0]['creatives']['openvideo']['content']",

        "root['ads'][0]['ad'][0]['ext']['expiretime']",
        "root['MultiClickThrough'][0]['text']" #deeplink下发的url有个字段是可变的
    }
    diff_data = DeepDiff(expected_request, api_response, ignore_order=True, exclude_paths=exclude_paths)
    allure.attach(name="diff", body=str(diff_data))
    check_diff(diff_data)