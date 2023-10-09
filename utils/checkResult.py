"""
-*- coding: utf-8 -*-
@Time : 2023/9/25 
@Author : liuyan
@function : 
"""
import operator
import re
import allure

from utils.readExpectedResult import read_json


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


def check_result(test_name, case, code, data, _path, relevance=None):
    if case["check_type"] == 'no_check':
        with allure.step("不校验结果"):
            pass
    elif case["check_type"] == 'json':
        expected_request = case['expected_request']
        if isinstance(case["expected_request"], str):
            expected_request = read_json(test_name, expected_request, _path)
        with allure.step("JSON格式校验"):
            allure.attach(name="期望code", body=str(case["expected_code"]))
            allure.attach(name="期望data", body=str(expected_request))
            allure.attach(name="实际code", body=str(code))
            allure.attach(name="实际data", body=str(data))
        if int(code) == case["expected_code"]:
            if not data:
                data = "{}"
            check_json(expected_request, data)
        else:
            raise Exception("HTTP状态码错误！")

    elif case["check_type"] == 'only_check_status':
        with allure.step("仅校验HTTP状态码"):
            allure.attach(name="期望code", body=str(case["expected_code"]))
            allure.attach(name="实际code", body=str(code))
            allure.attach(name="实际data", body=str(data))
        if int(code) == case["expected_code"]:
            pass
        else:
            raise Exception("HTTP状态码错误！")

    elif case["check_type"] == 'entirely_check':
        expected_request = case['expected_request']
        if isinstance(case["expected_request"], str):
            expected_request = read_json(test_name, expected_request, _path)
        with allure.step("全量校验"):
            allure.attach(name="期望code", body=str(case["expected_code"]))
            allure.attach(name="期望data", body=str(expected_request))
            allure.attach(name="实际code", body=str(code))
            allure.attach(name="实际data", body=str(data))
        if int(code) == case["expected_code"]:
            result = operator.eq(expected_request, data)
            if result:
                pass
            else:
                raise Exception("完全校验失败！")
        else:
            raise Exception("HTTP状态码错误！")

    # elif case["check_type"] == 'Regular_check':