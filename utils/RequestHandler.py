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
from utils.XxteaHandler import Xxtea


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
#     base_url = 'https://cis.sohu.com/cisv4/feeds'
#     pre_url = 'http://t3.m.sohu.com/cisv4/feeds'
#
#     paramater = {
#     "suv":"220105104324TCFL",
#     "pvId":"1645169455057GplDHeH_46903",
#     "clientType":1,
#     "resourceParam":[
#         {
#             "requestId":"1645169455343_22010510432_cWA",
#             "resourceId":"1645169455343455619",
#             "page":1,
#             "size":20,
#             "spm":"smpc.topic_142.tpl-pc-feed-new",
#             "context":{
#                 "pro":"0,1",
#                 "feedType":"XTOPIC_SYNTHETICAL"
#             },
#             "resProductParam":{
#                 "productId":202,
#                 "productType":14
#             },
#             "productParam":{
#                 "productId":202,
#                 "productType":14,
#                 "categoryId":"40",
#                 "mediaId":1
#             }
#         }
#     ]
# }
#
#     paramater1 = {
#         "suv": "220105104324TCFL",
#         "pvId": "1645169455057GplDHeH_46903",
#         "clientType": 1,
#         "resourceParam": [
#             {
#                 "requestId": "1645169455343_22010510432_cWA",
#                 "resourceId": "1645169455343455619",
#                 "page": 1,
#                 "size": 20,
#                 "spm": "smpc.topic_142.tpl-pc-feed-new",
#                 "context": {
#                     "pro": "0,1",
#                     "feedType": "XTOPIC_SYNTHETICAL"
#                 },
#                 "resProductParam": {
#                     "productId": 203,
#                     "productType": 14
#                 },
#                 "productParam": {
#                     "productId": 203,
#                     "productType": 14,
#                     "categoryId": "40",
#                     "mediaId": 1
#                 }
#             }
#         ]
#     }
#     res1 = request_url.request_main('post', base_url, json=paramater)
#     res2 = request_url.request_main('post', pre_url, json=paramater1)
#     print(res1.text)
#     print(res2.text)
#     print(DeepDiff(json.loads(res1.text), json.loads(res2.text)))
