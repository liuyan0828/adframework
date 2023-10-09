"""
-*- coding: utf-8 -*-
@Time : 2021/12/6
@Author : liuyan
@function : 处理url
"""

from furl import furl


class UrlHandler(object):
    def __init__(self, url):
        self.f = furl(url)

    def get_host(self):
        """
        :return: 返回host
        """
        # f = furl(url)
        return self.f.host

    def get_all_params(self):
        """
        :return: 字典形式返回url中所有参数值，如无参数返回{}
        """
        # f = furl(url)
        return self.f.args

    def get_all_keys(self):
        """
        :return: 返回参数值中所有的key
        """
        params = self.get_all_params()
        return params.keys()

    def get_all_values(self):
        """
        :return: 返回参数值中所有的value
        """
        params = self.get_all_params()
        return params.values()

    def get_value(self, key):
        """
        :param key: 需要获取的key值
        :return: 获取参数值中特定key的value
        """
        params = self.get_all_params()
        if params:
            if key in params.keys():
                return params[key]
            else:
                return "该url中无对应key，请检查输入"
        else:
            return "该url无参数值"

    def set_value(self, key, value):
        """
        :param key: 需要替换value的key
        :param value: 替换后value值
        :return: 替换参数值中特定key的value
        """
        params = self.get_all_params()
        if params:
            if key in params.keys():
                params[key] = value
                self.f.args = params
                return self.f.url
            else:
                return "该url中无对应key，请检查输入"
        else:
            return "该url无参数值"

    def delete_params(self, key):
        """
        :param key: 需要删除的key值
        :return: 删除特定key:value对
        """
        params = self.get_all_params()
        if params:
            if key in params.keys():
                del params[key]
                return self.f
                # return params
            else:
                return "该url中无对应key，请检查输入"
        else:
            return "该url无参数值"

    def delete_specified_params(self, host_list, key_list):
        """
        :param host_list: 指定需要执行删除的host
        :param key_list: 指定需要删除的key
        :return: 返回删除对应参数后的url
        """
        host = self.get_host()
        if isinstance(host_list, (str, list)):
            if host == host_list or host in host_list:
                if isinstance(key_list, str):
                    self.delete_params(key_list)
                    return self.f.url
                elif isinstance(key_list, list):
                    for i in key_list:
                        self.delete_params(i)
                    return self.f.url
                else:
                    return "指定删除的key必须为str或list类型，请检查输入"
            else:
                # print("该url无需执行删除操作")
                return self.f.url
        else:
            return "指定删除的host必须为str或list类型，请检查输入"


# if __name__ == '__main__':
#     url = 'http://sohutv.m.cn.miaozhen.com/x/k=flow2impmma&p=7K3BW&dx=&rt=2&ns=123.126.70.235&ni=SOHU_650888&v=__LOC__&xa=__ADPLATFORM__&tr=cebc5050718749d00832997ce155f5ec_2073965902&mo=0&m0=&m0a=__DUID__&m1=__ANDROIDID1__&m1a=826906001476e7be6cf9ffe11936ea3e&m2=ed3b206647a84913200098a55d04836b&m4=__AAID__&m5=&m6=__MAC1__&m6a=05c89193236d709ce2d1411844d71771&nd=5055596&np=__POS__&nn=__APP__&nc=__VID__&nf=__FLL__&ne=__SLL__&ng=__CTREF__&nx=cm1XRlZNUVZwRlRVeG5TekUxTkRNNE1UZzBPVGslM0Q=&o='
#     handle_url = UrlHandler(url)
#     print(handle_url.get_host())
#     print(handle_url.get_all_params())
#     print(handle_url.get_all_keys(url))
#     print(handle_url.get_all_values(url))
#     print(handle_url.get_value(url, '111'))
#     print(handle_url.delete_params('encd'))
#     print(handle_url.delete_specified_params(['mmgtest.aty.sohu.com', 'mmg.aty.sohu.com'], ['encd', 'rt', 'sign']))
#     print(handle_url.get_all_params())

