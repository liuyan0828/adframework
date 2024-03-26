"""
@Time ： 2024/3/26
@author ：liuyan
"""
import pytest
from main import project_path
from utils.ReadYaml import read_yaml_files
from libs.checkResult import *


PATH = project_path + '/script/mad'
case_dict = read_yaml_files(PATH)


@allure.feature("中插")
class Test_Ad_Oad():
    @allure.story("校验xml是否能返回：1、返回是否是空广告 2、校验返回ad是否与基准一致 3、完全校验")
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    @pytest.mark.parametrize("case_data", case_dict[0], ids=case_dict[1])
    def test_ad_xml(self, case_data):
        allure.title(f"{case_data['title']}")
        # prot=vast则返回xml
        case_data['parameter']['prot'] = 'vast'
        res = check_code(case_data)
        res_data = RequestHandler.decode_xml_to_dict(res.content)
        assert res_data != {}
        # xml存放路径
        path = PATH + '/' + case_data['info'] + '/' + case_data['check']['expected_xml']
        base_xml = CompareXml.get_root(path)
        expected_request = CompareXml.get_all_elements(base_xml)
        root = ET.XML(res_data)
        api_response = CompareXml.get_all_elements(root)
        check_xml_res(expected_request, api_response)
