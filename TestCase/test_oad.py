"""
@Time ： 2024/2/21
@author ：liuyan
"""
import pytest
from main import project_path
from utils.ReadYaml import read_yaml_files
from utils.readExpectedResult import *
from libs.GetAdConf import *
from libs.checkResult import *


PATH = project_path + '/script/oad'
case_dict = read_yaml_files(PATH)


@allure.feature("前贴")
class Test_Ad_Oad():
    @allure.story("校验xml是否能返回")
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    @pytest.mark.parametrize("case_data", case_dict[0], ids=case_dict[1])
    def test_ad_xml(self, case_data):
        allure.title(f"{case_data['title']}")
        # xml存放路径
        path = PATH + '/' + case_data['info'] + '/' + case_data['check']['expected_xml']
        check_xml_res(case_data, path)
