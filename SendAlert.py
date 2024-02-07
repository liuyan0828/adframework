"""
-*- coding: utf-8 -*-
@Time : 2023/10/9 
@Author : liuyan
@function : 
"""
import gettext
import json
import requests
import jsonpath


class JsonHandle:
    def json_to_dict(self, url, encoding="UTF-8"):
        """
        :param url: 获取json结果的url
        :return: 返回转换成字典后的数据
        """
        json_data = requests.get(url=url).content.decode("utf-8")
        json_data = json.loads(json_data)
        # json_obj = json.load(json_obj) 从文件中取数据
        return json_data


class GetErrorMessage:
    def get_errormessage(self, categories_json):
        """
        :param categories_json: 报错信息
        """
        errorName = jsonpath.jsonpath(categories_json, '$..[?(@.status== "' + 'failed' + '")].name')
        errorUid = jsonpath.jsonpath(categories_json, '$..[?(@.status== "' + 'failed' + '")].parentUid')

        case_name = [x[x.find('[')+1:x.find(']')] for x in errorName]
        case_error = [jsonpath.jsonpath(categories_json, '$..[?(@.uid== "' + x + '")].name') for x in errorUid]
        errorMessage = dict(zip(case_name, case_error))
        return errorMessage


class SendMarkdown:
    def send_markdown(self, wx_url, reportUrl, errorMesssge):
        """
        :param reportUrl: 报告链接
        :param errorMessage: 报错信息
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": "# **提醒！以下广告位接口返回失败**\n#### **请相关同事注意，及时跟进！**\n"
                           "> ##### **报告链接：** [jenkins报告,请点击后进入查看](%s) \n"
                           "> 详情: <font color=\"info\">%s</font> \n" % (
                               reportUrl, errorMesssge)
            }
        }
        content = data["markdown"]["content"]
        content_bytes = content.encode('utf-8')
        if len(content_bytes) > 4096:
            content_tmp = content_bytes[:4096]
            res = content_tmp.decode('utf-8', errors='ignore')
            data["markdown"]["content"] = res
        r = requests.post(wx_url, json=data)
        res = r.text


if __name__ == '__main__':
    base_url = 'http://10.33.4.109:8080/jenkins/job/ad_api_test/'
    # 获取jenkins的lastBuild号
    newid = str(requests.get(base_url + 'lastBuild/buildNumber').text)

    categories_url = base_url + newid + '/allure/data/categories.json'
    json_handle = JsonHandle()
    categories_json = json_handle.json_to_dict(categories_url)
    errorMesssge = GetErrorMessage().get_errormessage(categories_json)

    wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9230171b-f329-451f-8877-84bb4d298ca6"
    content = SendMarkdown()
    content.send_markdown(wx_url, base_url + newid + "/allure/#behaviors", errorMesssge)

