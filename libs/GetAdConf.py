"""
-*- coding: utf-8 -*-
@Time : 2024/1/18 
@Author : liuyan
@function : 
"""
import requests
import json


class GetAdConf():
    def __init__(self, payload):
        url = "http://mangotest3.aty.sohuno.com/api/d/advertisement/getEditListByGroupids"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Origin': 'http://mangotest3.aty.sohuno.com',
            'Connection': 'keep-alive',
            'Referer': 'http://mangotest3.aty.sohuno.com/mango'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()
            self.res = json.loads(response.text)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)

    # 获取广告模板
    def get_adtemplate(self):
        return self.res['rows'][0]['adtemplate']

    # 获取第三方跳转类型
    def get_redirecttype(self):
        return self.res['rows'][0]['redirectsList'][0]['type']

    # 获取第三方跳转
    def get_redirecturl(self):
        return self.res['rows'][0]['redirectsList'][0]['url']

    # 获取点击触发类型
    def get_clicktype(self):
        return self.res['rows'][0]['clickType']

    # 获取点击按钮文字
    def get_buttontext(self):
        return self.res['rows'][0]['buttontext']

    # 获取是否deeplink
    def get_isdeeplink(self):
        return self.res['rows'][0]['isdeeplink']

    # 获取硬广广告标识
    def get_hardadflag(self):
        return self.res['rows'][0]['hardadflag']

    # 获取是否过滤重复点击
    def get_dropInvalidClick(self):
        return self.res['rows'][0]['dropInvalidClick']

if __name__ == '__main__':
    payload = "groupids=24508&maIds="
    print(GetAdConf(payload).get_adtemplate())
    print(GetAdConf(payload).get_redirecttype())
    print(GetAdConf(payload).get_redirecturl())
    print(GetAdConf(payload).get_clicktype())
    print(GetAdConf(payload).get_buttontext())
    print(GetAdConf(payload).get_isdeeplink())
    print(GetAdConf(payload).get_hardadflag())
    print(GetAdConf(payload).get_dropInvalidClick())