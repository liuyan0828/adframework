"""
-*- coding: utf-8 -*-
@Time : 2023/9/25 
@Author : liuyan
@function : 
"""

import json
from json import JSONDecodeError


def read_json(test_names, code_json, _path):
    try:
        with open(_path+'/'+code_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # for i in data:
            #     if i['test_name'] == test_names:
            #         code_json = i['json']
            #         break
            # if not code_json:
            #     raise Exception('未找到对应测试用例{}关联的期望文件：{}'.format(test_names, _path+'/'+code_json))
    except FileNotFoundError:
        raise Exception('未找到对应测试用例关联的期望文件：{}'.format(code_json))
    except JSONDecodeError:
        raise Exception('期望文件{}格式错误'.format(code_json))
    return data