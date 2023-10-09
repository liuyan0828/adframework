"""
-*- coding: utf-8 -*-
@Time : 2021/12/8
@Author : liuyan
@function : 请求url获取返回数据
"""

from utils.RequestHandler import RequestHandler
from libs.Config import URL_CONFIG
from utils.UrlHandler import UrlHandler


class GetAdData(object):
    @staticmethod
    def get_ad_data(ad_url):
        """得到广告返回的json数据
        ad_url:广告访问链接，例如：mf?site=1&p=7&v=137006183&vl=1200&td=&vs=1.0&ct=a&cs=
        """
        url = URL_CONFIG['APP_AD_URL'] + ad_url
        get_data = RequestHandler()
        ad_data = get_data.request_main("get", url)
        return ad_data

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
        """
        :return: 获取请求链接中aid视频status；如视频不存在返回10001，如存在返回200
        """
        # 获取请求链接中的aid
        aid = UrlHandler(URL_CONFIG['APP_AD_URL'] + ad_url).get_value('al')
        get_data = RequestHandler()
        tvapi_url = URL_CONFIG['TVAPI_URL']
        # 将tvapi_url中的al替换为aid并发起请求，获取返回值
        ad_data = get_data.request_main("get", tvapi_url.replace('al', aid)).json()
        return ad_data['status']


# ad_url = "m?pt=flogo&source=1000180001&huawei_hms_version=60400302&userid=0&vid=5161723&du=2592.894&plat=6&UUID=d8a3986d-b8fd-440a-b67d-cfc6eb4351861646897330839&ext=2097151&qt=0&islocaltv=0&al=999654&replay=0&vc=101141;101147;101148&protv=3.0&adoriginal=sohu&broadcastID=0&guid=d2b2c28b7634dc0a25318b6c7d8ab003&sdkVersion=tv8.3.42&isroot=false&vu=0&channeled=1000180001%7C3810&gid=x0107402101014d7580e4084b0007e36f04e5fb05a0f&frontAdsTime=185&privacy=1&forbid=0&playstyle=1&battery=27&exten=1,2,3,4,5,6,7,8&offline=0&huawei_store_version=120001301&prot=vast&encrypt=N3DCTlohFC5TXYoOkqmTXdFJUZ31C79ILomyXJCLbYHNKkZZufgyMjGkjQ0ewILwa%2FP9jWhLV40%3D&isBgPlay=0&player=1&c=tv&density=3.0&displayMetrics=1080*2340&encd=ZdXLMuuNXsn%2Bgp%2BB4o%2B0EkmLdSxlHJvUqvAbSMmgxjzT9GODKy6Bt7i37mKrs0uMt66bkRv0e%2BZvZn2BIaExsO3p5uBdCXV31cg7hknu%2FXImpRc0%2Bb58Xar6513sp48CfhwbO1TIuyWXYzbmdnHoj9AiM2eg1Q6G5Vfhf9W5PvUqK3BF%2BNM1%2FpeC78sSxmVo%2FFFupINJb4z6nHxZXr%2FgYQeKn0XKNEwFv6Ux0RXEchTyHZJ0klRlzo1N990uNDYYLTH37Ksx1AkUInMwBtvV37bPIU088q%2B3L19UtRxkzY2l2ovEpBB7IZqTZFZsP8pMZmZUWXzjYS6%2Fi%2BJ3dRuVOoaKH9ByMkaWkKcwhwABxS%2BL90sH0wea6MeaVinGHxucsvlqF6zZ4Ak2ZSCwIIY1a9iwbdAUOuIDDGrywg9bUKbLzwYG7GAe3eAELxVSRCoeBfbiwBn%2F8c%2Bwi232VRE5gWlSST9nu1zjjmYID7S4GfFgBm8w4LKj4F0bYK75oPTVrmItd82eqE3dINtxNGTSj9ybvekhd4dSLE8dBB4PJQKImX7JjRHZrxzTpQM0cok3Nr6eYFkk1HuEW14VF5owlxS9VH%2BK4l5thb9iy7bSsUqNPfGeXQSWvodJFwEkQCqk%2BSPVvOge3%2F1rUe94WPFAUDuqGk0kta2RJmS%2Fcerb2wrbnKROdD6IAA5bAoqDgKOhrMvZUA1JSqor4wmPxQQep4zuLmD3EktHSJQ5RQzHgQ8Tk5mpovRuMSC736lGrQhv%2F3nJ2lHGKAwMHt7qiuLVhqeH6Bx9UYl6PGhWrBsjW4GeAE8bE5Vk6XMLlDMW4347Vh7eUQ%3D%3D&sver=9.6.21&playerScale=0.5625&poid=1&audited_level=-1&uptime=13613536&site=1&partner=93&build=9.6.21&appid=tv"
# res = GetAdData.get_tvapi_data(ad_url)
# print(res)