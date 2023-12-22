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


if __name__ == '__main__':
    url = "http://mmg.aty.sohu.com/goto?du=0&rt=1700032799115_6559_10.33.8.134_15_15&spead=0&plat=3&sver=9.9.20&poid=1&adplat=2&prot=json&protv=3.0&build=com.sohu.inhouse.iphonevideo&appid=tv&adoriginal=sohu&sdkVersion=15.9.1&offline=0&density=2.000000&displayMetrics=375*667&bt=20231115&endtime=20231231&ad=54962&b=417762&bk=117199509&pagetype=2&islocaltv=0&seq=1&w=1080&h=1920&wdbn=1080&hgbn=1920&cheattype=0&sperotime=1700032799&site=1&template=video&platsource=tv&indexip=adveng-retrvl-qa.ns-adveng-qa.svc.cluster.local:60111&backtest=ctr_cheat,pacing_ad_alloc_a,exp_nobidfloor,pdb_load_a,pdb_opt_a&ispgc=0&impressionid=7528c6f1f2089fe9a5e9dc4a70456d2d&scope=0&flightid=36609765&from=tvssp&advertiserid=11635&encd=92I3jLba%2FU8Tivxo0cfnxsGaxS0pwzAx9oO%2FNuFkHj6UXrQcMXwZW%2F0NPfH2QwiybpqwJqyftA1LozHeFj61jqs3U07L6anVRF%2FRZlASkCbNExR6QnM0%2FhhbC6TXvdkQKcwTUx05wkGgkhcFBO4yJio6hpIRGtcKXue2Wp76oByPpYD%2F2u1cdme7H%2FZExrh5IWzwb1ruZFkNChV%2FEs7QlZ0vrzJ8c260E6ngocShU1hjNZCMri4e8lWczTGrGTElL20lPoIfsUG6D8JNeBZ%2BZm%2Bqww%2Bsyd1D50tHcbOw5GOHOpFk1IhAna8%2FRm8cCbJMiCiUTpDYLZuE0c96iGqBYnqU%2BtSgIugMekH2yrTpx9iPpAYtbRVK7C8JPrX1sYPAexQRUikYg%2F0ddLYFyMPw2C1WR9fKvY6VpnfXOzerIgfSv%2BiKEzVUvn2igUimxsyVmb0ZVAKQBgAenHsrZP6JO6U20yI%3D&err=[ERRORCODE]&dx=__DOWN_X__&dy=__DOWN_Y__&ux=__UP_X__&uy=__UP_Y__&at=0&c=2741&p=op&posid=op_iphone_1&loc=Unknown&adstyle=open&ac=5487&ad=54962&pt=12621&b=417762&bk=117199509&pagetype=2&spead=0&eventtype=deeplink"
    handle_url = UrlHandler(url)
    print(handle_url.get_host())
    print(handle_url.get_all_params())
    # print(handle_url.get_all_keys(url))
    # print(handle_url.get_all_values(url))
    # print(handle_url.get_value(url, '111'))
    # print(handle_url.delete_params('encd'))
    # print(handle_url.delete_specified_params(['mmgtest.aty.sohu.com', 'mmg.aty.sohu.com'], ['encd', 'rt', 'sign']))
    # print(handle_url.get_all_params())

