"""
-*- coding: utf-8 -*-
@Time : 4/9/25 
@Author : liuyan
@function : 
"""
import json
from jsonschema import validate, ValidationError
import allure

def check_response_schema(response_data, schema_path):
    """
    校验 response 是否符合指定 jsonschema
    """
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    with allure.step("校验返回结构是否符合 schema"):
        try:
            validate(instance=response_data, schema=schema)
        except ValidationError as e:
            allure.attach(name="Schema 校验失败信息", body=str(e))
            assert False, f"❌ Schema 校验失败：{e.message}"
