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
                    return self.f
                elif isinstance(key_list, list):
                    for i in key_list:
                        self.delete_params(i)
                    return self.f
                else:
                    return "指定删除的key必须为str或list类型，请检查输入"
            else:
                # print("该url无需执行删除操作")
                return self.f
        else:
            return "指定删除的host必须为str或list类型，请检查输入"


# if __name__ == '__main__':
#     url = 'http://mmg.aty.sohu.com/madfail?du=2725&adtime=75&trule=37984&mx=5&al=9622743&vid=6102990&tvid=177372077&spead=8&uv=ad9b3a32-cffd-488b-8d41-5ea01134a6b1&uuid=846c06d0-1791-4c8e-8882-87d3a79ac496&UUID=846c06d0-1791-4c8e-8882-87d3a79ac496&crid=0&ar=6&rip=10.2.146.77&sip=10.18.40.254&plat=6&sver=9.2.20&partner=93&poid=1&pn=VOG-AL00&sysver=29&adplat=3&source=1000080005&wt=WIFI&v1=1048&v1code=101&v2code=101148&prot=vast&protv=3.0&playstyle=1&build=9.2.20&appid=tv&adoriginal=sohu&sdkVersion=tv7.7.10-SNAPSHOT&offline=0&density=3.0&displayMetrics=1080%2A2340&islocaltv=0&datatype=2&bssid=02%3A00%3A00%3A00%3A00%3A00&ssid=%3Cunknown+ssid%3E&endtime=20231231&pagetype=1&supplyid=8&suid=ad9b3a32-cffd-488b-8d41-5ea01134a6b1&mac=F6%3AE7%3AA5%3AB3%3A2E%3A58&AndroidID=ec91f6f6916f7c0e&islocaltv=0&manufacturer=HUAWEI&guid=76b516d09e1a54b0df00255ed4103dd4&imsi=null&seq=1&cheattype=16&sperotime=1639377478&tuv=SV_XacejO3AzKksKxHFCanHEq7lahna-Y0lPZ2T2OmICoqSpPN4whGO28JlBg8D5Xdc&site=1&template=skip%2Cnull&platsource=tv&indexip=127.0.0.1%3A60111&channeled=1000080005&vu=0&vc=101147%3B101148&vp=s&at=15&c=1&v1=1048&p=oad1%2Coad2%2Coad3%2Coad4%2Coad5&loc=Unknown&adstyle=oad&ac=5479&ad=54359&pt=12612&b=415418&bk=113830252&pagetype=1&te=2&spead=8&err=%5BERRORCODE%5D&encrysig=lVUqoJj2mcCfN2P2uEgsCfZjCrv5P-yn24E2ySXN8o8dAY6v'
#     handle_url = UrlHandler(url)
#     print(handle_url.get_host())
#     print(handle_url.get_all_params())
#     print(handle_url.get_all_keys(url))
#     print(handle_url.get_all_values(url))
#     print(handle_url.get_value(url, '111'))
#     print(handle_url.delete_params('encd'))
#     print(handle_url.delete_specified_params(['mmgtest.aty.sohu.com', 'mmg.aty.sohu.com'], ['encd', 'rt', 'sign']))
#     print(handle_url.get_all_params())

