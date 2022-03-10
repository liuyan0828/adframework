"""
-*- coding: utf-8 -*-
@Time : 2021/12/7
@Author : liuyan
@function : 对比两个xml文件的异同
"""

from libs.GetAdData import GetAdData
import xml.etree.ElementTree as ET
from libs.UrlHandler import UrlHandler


class CompareXml(object):

    @staticmethod
    def get_root(filepath):
        tree = ET.parse(filepath)
        return tree.getroot()

    @staticmethod
    def get_all_elements(root):
        """
        处理值，去除其中的\t\n字符，如果是http开头的字符串，去除指定host中的指定字段，如果是None，设置为空字符串
        :return: 返回xml文件中所有的子节点,格式为[tag名, 属性， 值]
        """
        ele_list = []
        for i in root.iter():
            if i.tag != "ExpireTime":
                if i.text:
                    i.text = i.text.replace("\t", "").replace("\n", "")
                if i.text is None:
                    i.text = ''
                i.text = i.text.strip()
                if i.text.startswith('http'):
                    handle_url = UrlHandler(i.text)
                    i.text = handle_url.delete_specified_params(['mmgtest.aty.sohu.com', 'mmg.aty.sohu.com'], ["vu",'du','appid','encd',"cheattype", 'rt','platsource', 'sign','warmup','rip', 'fip', 'v2code', 'bt','backtest','bk', 'sperotime',"impressionid","flightid","sspreqid"])
                ele_list.append([i.tag, i.attrib, i.text])
        return ele_list

    @staticmethod
    def compare_elements(base_el, cur_el):
        """
        :param base_el: 基准xml文件的子节点列表
        :param cur_el: 需要对比的xml文件子节点列表
        :return: 返回差异点
        """
        # 对比基准xml多余的元素列表
        extra_ele = [i for i in cur_el if i not in base_el]
        # 对比基准xml缺少的元素列表
        lack_ele = [j for j in base_el if j not in cur_el]
        # 标志文件是否一致，如一致，flag为1
        flag = 0

        base_tag = list(i[0] for i in base_el)
        cur_tag = list(i[0] for i in cur_el)
        if extra_ele == [] and lack_ele == []:
            # 如果不存在多余字段也没有缺少字段，且所有子节点tag顺序一致，则认为2个文件一致
            if base_tag == cur_tag:
                flag = 1
            else:
                print('两文件字段及对应属性值均一致，但结构不一致')

        for i in extra_ele:
            for j in lack_ele:
                #  如果存在相同tag值的元素，找出该tag值属性和text的不同点
                if len(i) != 0 and len(j) != 0:
                    if i[:1] == j[:1]:
                        if i[2] != j[2]:
                            if not isinstance(i[2], str) and not isinstance(i[2], str):
                                print('{}的text值存在差异'.format(i[0]))
                                host1 = UrlHandler(i[2]).get_host()
                                host2 = UrlHandler(j[2]).get_host()
                                if host1 != host2:
                                    print('其中host不同，基准为{}，但实际为{}'.format(host1, host2))
                                params1 = UrlHandler(i[2]).get_all_params()
                                params2 = UrlHandler(j[2]).get_all_params()
                                lack_key = []
                                for k, v in params1.items():
                                    if k not in params2.keys():
                                        lack_key.append({k:v})
                                    if k in params2.keys():
                                        if v != params2[k]:
                                            print('其中{}值不同，基准为{}，但实际为{}'.format(k, params2[k], params1[k]))
                                if lack_key:
                                    print("测试文件的该字段缺少参数：{}".format(lack_key))
                                extra_key = []
                                for k, v in params2.items():
                                    if k not in params1.keys():
                                        extra_key.append({k:v})
                                if extra_key:
                                    print("测试文件的该字段多余参数：{}".format(lack_key))
                            else:
                                print('{}的text值存在差异: 基准text为{}，但实际text为{}'.format(i[0], i[2], j[2]))
                            i.clear()
                            j.clear()
                    elif i[1] != j[1]:
                        if i[2] == j[2]:
                            print('{}的属性值存在差异：基准属性值为{}，但实际属性值为{}'.format(i[0], i[1], j[1]))
                        else:
                            print('{}的属性值及text均存在差异：基准属性值为{}，但实际属性值为{}'.format(i[0], i[1], j[1]))
                            print('基准text为{}，但实际text为{}'.format(i[2], j[2]))
                            i.clear()
                            j.clear()
        while [] in extra_ele:
            extra_ele.remove([])
        while [] in lack_ele:
            lack_ele.remove([])
        if extra_ele:
            print("当前测试xml文件多余字段，具体字段信息如下: ")
            for i in extra_ele:
                print(i)
        if lack_ele:
            print("当前测试xml文件缺少字段，具体字段信息如下: ")
            for j in lack_ele:
                print(j)
        return flag







