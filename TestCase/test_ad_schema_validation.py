"""
-*- coding: utf-8 -*-
@Time : 4/9/25 
@Author : liuyan
@function : 
"""
import allure
from utils.schema_checker import check_response_schema
from api.get_ad_data import get_ad_data  # 你自己的请求模块
from config import URL_CONFIG  # 请求地址

@allure.epic("广告接口结构校验")
@allure.feature("使用 jsonschema 校验广告字段结构")
@allure.story("返回字段结构是否合规")
def test_ad_schema_validation():
    """
    实战用例：发送广告请求并验证返回结构
    """
    # 发送广告请求
    url = URL_CONFIG['APP_AD_URL'] + "/your_ad_path_here"
    response = get_ad_data(url)  # 返回 json 数据
    response_data = response.json()

    # 校验结构
    schema_path = "schemas/ad_response_schema.json"
    check_response_schema(response_data, schema_path)

