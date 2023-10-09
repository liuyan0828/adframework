# -*- coding: utf-8 -*-

import pytest
import os
import sys

project_path = os.path.split(os.path.realpath(__file__))[0]

if ':' in project_path:
    project_path = project_path.replace('\\', '/')
else:
    pass


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    

    # s输出打印信息，v输出详细信息。不指定则运行所有

    args = ['-s', '-q', 'TestCase', '--alluredir', 'Report/xml_report', '--clean-alluredir']
    exit_code = pytest.main(args)
    if exit_code == pytest.ExitCode.OK:
        exit(0)
    else:
        exit(1)

    os.system('allure generate %s -o %s --clean' % ('Report/xml_report', 'Report/html_report'))


    # 运行指定模块
    # pytest.main(['-vs', 'test_gphone_oadKeTiaoGuo.py'])

