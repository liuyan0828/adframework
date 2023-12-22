"""
-*- coding: utf-8 -*-
@Time : 2023/9/14 
@Author : liuyan
@function : 
"""
import os
import shutil

from utils.MakeDir import mk_dir
from script.WriteCaseYaml import write_case_yaml
from main import project_path


def write_case(_path):
    case_path = project_path + '/script'
    # 根据charles文件生成yaml文件
    yaml_list = write_case_yaml(_path,  case_path)
    # 生成testcase路径
    test_path = project_path + '/TestCase'
    # 生成testcase的yaml模版路径
    src = case_path + "/Template.py"

    for case in yaml_list:
        yaml_path = case.split("/")[0]
        yaml_name = case.split("/")[1]
        case_name = 'test_' + yaml_name + '.py'
        new_case = test_path + '/' + case_name
        # mk_dir(test_path + yaml_path)
        if case_name in os.listdir(test_path):
            pass
        else:
            shutil.copyfile(src, new_case)
            with open(new_case, 'r', encoding='utf-8') as fw:
                source = fw.readlines()
            n = 0
            with open(new_case, 'w', encoding='utf-8') as f:
                for line in source:
                    if 'PATH = project_path' in line:
                        line = line.replace("offer", "%s" % yaml_path)
                        f.write(line)
                        n = n + 1
                    elif 'case_dict = read_yaml_file' in line:
                        line = line.replace("Template", yaml_name)
                        f.write(line)
                        n = n + 1
                    elif 'class TestTemplate' in line:
                        line = line.replace("TestTemplate", "Test%s" % yaml_path.title().replace("_", ""))
                        f.write(line)
                        n = n + 1
                    elif '@allure.story' in line:
                        line = line.replace("Template", yaml_name)
                        f.write(line)
                        n = n + 1
                    elif 'def test_template' in line:
                        line =line.replace("test_template", "test_%s" % yaml_name.lower())
                        f.write(line)
                        n = n + 1
                    else:
                        f.write(line)
                        n += 1

                for i in range(n, len(source)):
                    f.write(source[i])


if __name__ == '__main__':
    # charles文件地址
    har_path = project_path + '/charles_file'
    write_case(har_path)