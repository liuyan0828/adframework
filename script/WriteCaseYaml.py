"""
-*- coding: utf-8 -*-
@Time : 2023/9/12 
@Author : liuyan
@function : 
"""
import base64
import json
import os
import urllib.parse
import yaml
import logging

from utils.XxteaHandler import Xxtea
from utils.MakeDir import mk_dir
from main import project_path


def write_case_yaml(har_path, case_path):
    """
    循环读取Charles导出文件，生成yaml文件
    :param har_path: Charles导出文件路径
    :return:
    """
    har_list = os.listdir(har_path)
    case_file_list = []

    for i in har_list:
        if 'chlsj' in i:
            with open(har_path + '/' + str(i), 'r', encoding='utf-8') as f:
                logging.info('从{}目录下，开始读取文件：{}'.format(har_path, i))
                har_cts = json.loads(f.read())
                har_ct = har_cts[0]
                case_list = dict()
                scheme = har_ct['scheme']
                method = har_ct['method']
                path = har_ct['path']
                title = i.split('.')[-2]
                parameter_type = har_ct["request"]["mimeType"]
                parameter = dict()
                try:
                    if method in 'POST':
                        # urllib.parse.unquote 用于将 URL 编码的字符串解码为普通字符串
                        parameter_list = urllib.parse.unquote(har_ct["request"]["body"]["text"])
                    elif method in 'PUT':
                        parameter_list = har_ct["request"]["body"]["text"]
                    elif method in 'DELETE':
                        parameter_list = urllib.parse.unquote(har_ct["request"]["body"]["text"])
                    else:
                        parameter_list = har_ct["query"]
                    # print(parameter)
                    if '&' in parameter_list:
                        for key in parameter_list.split('&'):
                            val = key.split('=')
                            if len(val) == 2:
                                parameter[val[0]] = val[1]
                    else:
                        parameter = json.loads(parameter_list)

                except Exception as e:
                    logging.error('未找到parameter: {}'.format(e))
                    raise e

                case_dir = case_path + '/' + i.split('.')[-2] + '/'
                mk_dir(case_dir)

                response_code = har_ct["response"]["status"]
                response_body = har_ct["response"]["body"]["text"]
                # 如果返回是字符串（加密），解密返回
                if isinstance(response_body, str):
                    try:
                        res = bytes(response_body, encoding="utf-8")
                        xxtea = Xxtea()
                        k = u"Adp201609203059Y"
                        key = k.encode("ascii")
                        data = xxtea.decrypt(base64.b64decode(res), key)
                    except Exception as e:
                        raise Exception("转换失败：{}".format(e))
                response_boby = json.loads(data)

                check = dict()
                check["check_type"] = 'json'
                check["expected_code"] = response_code
                expected_request = response_boby

                result_file = 'result_' + title + '.json'
                if len(expected_request) >= 3:
                    if result_file in os.listdir(case_dir):
                        pass
                    else:
                        result_list = []
                        result_dicts = dict()
                        with open(case_dir + '/' + result_file, 'w', encoding='utf-8') as file:
                            result_dicts["test_name"] = title
                            result_dicts['json'] = expected_request
                            result_list.append(result_dicts)

                            json.dump(result_list, file, ensure_ascii=False, indent=4)
                    check['expected_request'] = result_file

                else:
                    check['expected_request'] = expected_request

                param_file = case_dir + '/' + title + '.json'
                test_case_list = []
                test_case = dict()
                test_case_list.append(test_case)
                # para参数大于等于4时，参数文件单独写入json中
                # if len(parameter) >= 4:
                #     if title + '.json' in os.listdir(case_dir):
                #         pass
                #     else:
                #         new_dicts = dict()
                #         new_list = []
                #         with open(param_file, "w", encoding='utf-8') as fs:
                #             new_dicts["test_name"] = title
                #             new_dicts["parameter"] = parameter
                #             new_list.append(new_dicts)
                #
                #             json.dump(new_list, fs, ensure_ascii=False, indent=4)
                #     test_case["parameter_json"] = title + '.json'

                test_case["parameter"] = parameter

                test_case["http_type"] = scheme
                test_case["request_type"] = method
                test_case["parameter_type"] = parameter_type
                test_case["timeout"] = 20
                test_case["check"] = check
                test_case["address"] = path
                test_case["info"] = title
                test_case["payload"] = "groupids="
                test_case["title"] = ""

                case_list["testcase"] = test_case_list

                case_file = case_dir + '/' + title + '.yaml'
                if title + '.yml' in os.listdir(case_dir):
                    pass
                else:
                    with open(case_file, 'w+', encoding='utf-8') as ff:
                        case_file_list.append(case_dir.split("/")[-2] + '/' + title)
                        logging.debug("从%s目录下，写入测试文件%s" % (case_dir, case_file))
                        yaml.dump(case_list, ff, Dumper=yaml.SafeDumper)
    return case_file_list


case_path = project_path + '/script'
har_path = project_path + '/charles_file'
print(write_case_yaml(har_path, case_path))