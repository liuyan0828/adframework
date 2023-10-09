"""
-*- coding: utf-8 -*-
@Time : 2021/12/7
@Author : liuyan
@function : 对比两个xml文件的异同
2022.5.27 更新 增加JSON处理
"""

import xml.etree.ElementTree as ET

from utils.UrlHandler import UrlHandler


class CompareXml(object):

    @staticmethod
    def get_root(filepath):
        tree = ET.parse(filepath)
        return tree.getroot()

    @staticmethod
    def get_all_elements(root, status):
        """
        处理值，去除其中的\t\n字符，如果是http开头的字符串，去除指定host中的指定字段，如果是None，设置为空字符串
        :return: 返回xml文件中所有的子节点,格式为[tag名, 属性， 值]
        """
        ele_list = {}
        for i in root.iter():
            if i.tag != ("ExpireTime" or "RemainClick"):
                if i.tag != "SupportUnion":
                    if i.text is None:
                        i.text = ''
                    i.text = i.text.strip()
                    if i.tag in ['Impression', 'CompanionClickTracking']:
                        if 'id' in i.attrib.keys():
                            if i.attrib['id'] in ['mma', 'miaozhen', 'admaster', 'other']:
                                h_url = UrlHandler(i.text)
                                i.text = h_url.get_host()
                                print(i.tag, i.attrib, i.text)
                    if i.text.startswith('http'):
                        handle_url = UrlHandler(i.text)
                        i.text = handle_url.delete_specified_params(['mmgtest.aty.sohu.com', 'mmg.aty.sohu.com'],
                                                                    ["vu", 'du', 'appid', 'encd', "cheattype", 'rt',
                                                                     'platsource', 'sign', 'warmup', 'rip', 'fip',
                                                                     'v2code', 'bt', 'backtest', 'bk', 'sperotime',
                                                                     "impressionid", "flightid", "sspreqid", "sip",
                                                                     "indexip", "v2","encrysig","dx","dy","ux","uy","pgcauthor","vc"])
                        i.text = handle_url.delete_specified_params(['data.vod.itc.cn'],
                                                                    ["sig","prod","new"])
                        if status == 10001:
                            i.text = handle_url.delete_specified_params(['mmgtest.aty.sohu.com', 'mmg.aty.sohu.com'],
                                                                        ["tvid", "crid", "ar", "datatype"])
                    if i.tag in ele_list.keys():
                        ele_list[i.tag].append({'att': i.attrib, 'text': i.text})
                    else:
                        ele_list[i.tag] = [{'att': i.attrib, 'text': i.text}]
        return ele_list


class JsonHandle:

    # 只支持字典、列表嵌套的数据格式
    @staticmethod
    def get_target_result(dic):
        """
        :param dic: 需要处理的数据
        :return: 处理后的dic
        """
        if not dic:
            return 'argv[1] cannot be empty'
        # 对传入数据进行格式校验
        if not isinstance(dic, dict) and not isinstance(dic, list):
            return 'argv[1] not an dict or an list '
        if isinstance(dic, dict):
            for k, v in dic.items():
                if isinstance(v, str) and v.startswith('http'):
                    handle_url = UrlHandler(v)
                    v = handle_url.delete_specified_params(['mmgtest.aty.sohu.com', 'mmg.aty.sohu.com'],
                                                                ["vu", 'du', 'appid', 'encd', "cheattype", 'rt',
                                                                 'platsource', 'sign', 'warmup', 'rip', 'fip', 'v2code',
                                                                 'bt', 'backtest', 'bk', 'sperotime', "impressionid",
                                                                 "flightid", "sspreqid","v1code","vc","sip"])
                    dic[k] = v
                if isinstance(v, list):
                    JsonHandle.get_target_result(dic[k])
        else:
            # 如果数据类型为列表，遍历列表调用get_target_result函数
            for j in dic:
                JsonHandle.get_target_result(j)
        return dic


