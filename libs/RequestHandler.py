"""
-*- coding: utf-8 -*-
@Time : 2021/12/6
@Author : liuyan
@function : requests请求封装及返回数据的处理
"""
import base64
import simplejson as json
import xmltodict
import requests
from libs.Xxtea import Xxtea


class RequestHandler(object):
    def __init__(self):
        self.session = requests.session()

    def request_main(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        """
        :param method: 请求方式
        :param url: 请求url
        :param params: 请求参数，如无不传即可
        :param data: 请求data，如无不传即可
        :param json: 请求json，如无不传即可
        :param headers: 请求头，如无不传即可
        :param kwargs: 可变参数
        :return: 返回请求结果
        """
        try:
            re = self.session.request(method, url, params=params, data=data, json=json, headers=headers, **kwargs)
        except Exception as e:
            raise Exception("请求{}失败，失败原因：{}".format(url, e))
        return re

    @staticmethod
    def xml_to_dict(re):
        """
        :param re: xml数据
        :return: 转换后的有序字典
        """
        try:
            re_dict = xmltodict.parse(re)
        except Exception as e:
            raise Exception("转换失败：{}".format(e))
        return re_dict

    @staticmethod
    def decode_xml_to_dict(re):
        """
        :param re: 加密后的xml
        :return: 转换后的有序字典
        """
        try:
            res = bytes(re)
            xxtea = Xxtea()
            k = u"Adp201609203059Y"
            key = k.encode("ascii")
            data = xxtea.decrypt(base64.b64decode(res), key)
            # re_dict = xmltodict.parse(data)
        except Exception as e:
            raise Exception("转换失败：{}".format(e))
        return data

    @staticmethod
    def json_to_dict(re):
        """
        :param re: json类型数据
        :return: 转换后的字典
        """
        try:
            re_dict = json.loads(re)
        except Exception as e:
            raise Exception("转换失败：{}".format(e))
        return re_dict

    def close_session(self):
        self.session.close()


# if __name__ == '__main__':
#     request_url = RequestHandler()
#     base_url = 'http://10.16.79.96:8080/jenkins/job/%E9%A6%96%E9%A1%B5%E7%BA%BF%E4%B8%8A%E7%9B%91%E6%8E%A7/'
#     # 获取jenkins的lastBuild号
#     newid = str(requests.get(base_url + 'lastBuild/buildNumber').text)
#
#     behaviors_url = base_url + newid + '/allure/data/behaviors.json'
#
#     res = request_url.request_main('post', behaviors_url)
#
#     response = res.content.decode("utf-8")
#
#     print(RequestHandler.json_to_dict(response))






