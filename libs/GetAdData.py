"""
-*- coding: utf-8 -*-
@Time : 2021/12/8
@Author : liuyan
@function : 请求url获取返回数据
"""

from libs.RequestHandler import RequestHandler
from libs.Config import URL_CONFIG
import requests
from urllib import parse
from urllib.parse import urlparse


class GetAdData(object):
    @staticmethod
    def get_ad_data(ad_url):
        """得到广告返回的json数据
        ad_url:广告访问链接，例如：mf?site=1&p=7&v=137006183&vl=1200&td=&vs=1.0&ct=a&cs=
        """
        url = URL_CONFIG['APP_AD_URL'] + ad_url
        get_data = RequestHandler()
        ad_data = get_data.request_main("get", url)
        return ad_data.content.decode('utf-8')

    @staticmethod
    def get_ad_decode_data(ad_url):
        """得到广告返回的解密json数据
        ad_url:广告访问链接，例如：mf?site=1&p=7&v=137006183&vl=1200&td=&vs=1.0&ct=a&cs=
        """
        url = URL_CONFIG['APP_AD_URL'] + ad_url
        get_data = RequestHandler()
        ad_data = get_data.request_main("get", url)
        res = get_data.decode_xml_to_dict(ad_data.content)
        return res

    @staticmethod
    def get_pc_ad_data(ad_url):
        """得到广告返回的json数据
        ad_url:广告访问链接，例如：mf?site=1&p=7&v=137006183&vl=1200&td=&vs=1.0&ct=a&cs=
        """
        url = URL_CONFIG['PC_AD_URL'] + ad_url
        get_data = RequestHandler()
        ad_data = get_data.request_main("get", url)
        return ad_data

    def get_tvapi_data(ad_url):
        url = "http://tvapi.sohuno.com/v4/video/info/vid.json?site=1&api_key=685b608d9b1fa03f089f698a2e5e6fb4&aid=al"

        def getDic(a):  # 将返回的链接变成字典
            b = a.split("&")
            b = b[1:]
            d = {}

            for i in b:
                c = i.split("=")
                d.update({c[0]: c[1]})
            return d

        ad_urlDic = getDic(ad_url)
        bits = list(parse.urlparse(url))
        temp = bits[2]
        temp = "/v4/video/info/" + ad_urlDic['vid'] + ".json"
        bits[2] = temp

        qs = parse.parse_qs(bits[4])
        qs['aid'] = ad_urlDic['al']
        bits[4] = parse.urlencode(qs, True)
        url = parse.urlunparse(bits)
        r = requests.get(url)
        r_json = r.json()
        status = r_json["status"]
        return status


# ad_url = "m?channeled=1000080005&gid=x010740210101455c2215a45b000ddad472a6c8dfe1e&pt=oad&frontAdsTime=185&privacy=1&source=1000080005&huawei_hms_version=60200302&forbid=0&playstyle=1&battery=19&exten=1,2,3,4,5,6,7,8&vid=6102990&du=2725.056&offline=0&huawei_store_version=110501300&prot=vast&encrypt=4qTGgSzhRTUwg7CgJR9srqgHQJ1HvL0zkqU6wwjqKgWbIrn3LoTC3g%3D%3D&isBgPlay=0&plat=6&UUID=846c06d0-1791-4c8e-8882-87d3a79ac496&ext=2097151&c=tv&density=3.0&displayMetrics=1080*2340&encd=g6mEf%2Fw3AWjvgWudW3FoKbxAnS2CnHNhygaYXdKe7vIUDiBNRRV4kD9zIpxwOCDRkjitSQ4E2W%2FdZ17WzpGcIs4J5v2Mk6mDxyDCAYC40uBW%2BHmhbEGNi3Qmn8BJwOXfwnqUTJ68Cnr8qkO2GBiiXUKoDhKVRJ1EAxGZKMReRJYCqRvfIrv%2BbzE59meGl842zqeJPE4h69JmV8v9BOYe8YQHedzabyIMvihPqZ2%2FtrgbWNuduzAgqgqoIs4OqAJp%2BsRsauCSmw7fnLOOiyDGmMxIL9W65Jk5rSNPJ1Rtjatu%2BsYkuGbz7AbLbEKWwQ1oF%2FQNhEkN1g3MWK6WtpX5PAh3otxYMD4ASQvrPNik9EUEXTsMEd6bXPzPH%2BToZyOGxzL18QbTyd4FuU6UjFH6YtAqiyE5WwJJpXrpJR8reNGqHrOlW0y0QnGzfCP6Wm0PGykKfvCxGewqcOwb%2FFQjfM6b0OYoEDWFjb%2F%2BjYUeLIqyvRxk4dEM7zaqQ1OAgdKhXEY%2BghInznpVPXGc45TBWLbJ8UbnE0dEwF1C6h8WXnPVAJtXWEg1rcsxLQ%2BUqtVmNTJxH7S8tvo%2BHo66%2BbdEELxTQHSLOTjBZ%2F%2FRiabHFStMQkzR7Cwkx3DMlSygpMD37tFKpIMb%2F0Xz3K874cyRjAoG9Xfzzar3e%2F7BLVBjwLUlFeTUnd8Rb1wqX21Fiedh9p11Ngux%2BG8yKmJEQfmipqgEkvwDCHbwQDbZTwndfL3m1%2BwHwgzsAHMoLezsHYE5gQWPfh8YfqcwgW4HB565dSAVKUHLMrkh0GGHU9bv0NuYvBGpvbU1KDfWLOSSmOXAE3BQLTLDxkdf7QsaBnoN6eK%2FQC7Zr45OD%2F2zcsTCXFiojYzZ&sver=9.2.20&islocaltv=0&al=9622743&vc=101147;101148&playerScale=0.5625&screenstate=1&poid=1&audited_level=-1&uptime=1772647531&protv=3.0&site=1&partner=93&adoriginal=sohu&build=9.2.20&broadcastID=0&appid=tv&guid=76b516d09e1a54b0df00255ed4103dd4&sdkVersion=tv7.7.10-SNAPSHOT&isroot=false&playerMetrics=1080*607&vu=0"
# res = GetAdData.get_ad_data(ad_url)
# print(type(res))