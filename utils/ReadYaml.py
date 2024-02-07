"""
-*- coding: utf-8 -*-
@Modified: 2023/8/4
@Author : liuyan
@function : 读取yaml文件
"""
import logging
import os
import logging
import yaml
from yaml import safe_load


def iterate_yaml_files(folder_path):
    """
    Iterate through all yaml files in the folder.
    :param folder_path:
    :return: 遍历，如果文件以.yaml结尾则加入"yaml_files"生成器中
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.yaml'):
                yield os.path.join(root, file)


def read_yaml_files(folder_path):
    """
    :param folder_path:
    :return: 读取每个yaml文件，生成一个列表，列表中包含多个字典，每个字典代表一个用例；另外，使用列表推导式提取所有字典中的id值
    """
    testcase = []
    for yaml_file in iterate_yaml_files(folder_path):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            # "safe_load"更安全，不会因为未知键而引发错误；然而，它也会忽略未知键，而"load"会将它们保留在结果字典中。
            data = safe_load(f)['testcase']
        testcase.extend(data)
    ids = [item['title'] for item in testcase if 'title' in item]
    return [testcase, ids]


def read_yaml_file(_path, case_file):
    try:
        with open(_path + '/' + case_file + '.yaml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data
    except FileNotFoundError:
        logging.error('File not found: {}'.format(_path + '/' + case_file))

# if __name__ == '__main__':
#     filename = r'/Users/liuyan/Desktop/ad_test_framework/script/iPhone_16109'
#     r = read_yaml_file(filename, 'iPhone_16109')
#     print(r)
