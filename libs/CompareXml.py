"""
-*- coding: utf-8 -*-
@Time : 2021/12/7
@Author : liuyan
@function : 对比两个xml文件的异同
"""

from GetAdData import GetAdData
import xml.etree.ElementTree as ET
from UrlHandler import UrlHandler


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
            if i.text:
                i.text = i.text.replace("\t", "").replace("\n", "")
            if i.text is None:
                i.text = ''
            i.text = i.text.strip()
            if i.text.startswith('http'):
                handle_url = UrlHandler(i.text)
                # s = handle_url.delete_specified_params(['mmgtest.aty.sohu.com', 'mmg.aty.sohu.com'],'encd')
                i.text = handle_url.delete_specified_params(['mmgtest.aty.sohu.com', 'mmg.aty.sohu.com'], ['encd', 'rt', 'sign', 'rip', 'fip', 'v2code', 'bt', 'bk', 'sperotime'])
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
                if i[0] == j[0]:
                    if i[1] == j[1]:
                        if i[2] != j[2]:
                            print('{}的text值存在差异：基准text为{}，但实际text为{}'.format(i[0], i[2], j[2]))
                            params1 = UrlHandler(i[2]).get_all_params()
                            params2 = UrlHandler(j[2]).get_all_params()
                            for k, v in params1.items():
                                if k in params2.keys():
                                    if v != params2[k]:
                                        print('{}的text值存在差异：其中{}值不同，基准为{}，但实际为{}'.format(i[0], k, params2[k], params1[k]))
                    else:
                        if i[2] == j[2]:
                            print('{}的属性值存在差异：基准属性值为{}，但实际属性值为{}'.format(i[0], i[1], j[1]))
                        else:
                            print('{}的属性值及text均存在差异：基准属性值为{}，但实际属性值为{}'.format(i[0], i[1], j[1]))
                            print('基准text为{}，但实际text为{}'.format(i[2], j[2]))
                    # 如果两个列表都存在此tag，删除此tag字段
                    if i in extra_ele:
                        del extra_ele[extra_ele.index(i)]
                    if j in lack_ele:
                        del lack_ele[lack_ele.index(j)]
        if extra_ele:
            print("当前测试xml文件多余字段，具体字段信息如下: ")
            for i in extra_ele:
                print(i)
        if lack_ele:
            print("当前测试xml文件缺少字段，具体字段信息如下: ")
            for j in lack_ele:
                print(j)
        return flag


# if __name__ == '__main__':
#     base_xml = CompareXml.get_root(r"../基准xml/gphone前贴可跳过数据返回.xml")
#     base_el = CompareXml.get_all_elements(base_xml)
#     ad_url = "m?channeled=1000080005&gid=x010740210101455c2215a45b000ddad472a6c8dfe1e&pt=oad&frontAdsTime=185&privacy=1&source=1000080005&huawei_hms_version=60200302&forbid=0&playstyle=1&battery=19&exten=1,2,3,4,5,6,7,8&vid=6102990&du=2725.056&offline=0&huawei_store_version=110501300&prot=vast&encrypt=4qTGgSzhRTUwg7CgJR9srqgHQJ1HvL0zkqU6wwjqKgWbIrn3LoTC3g%3D%3D&isBgPlay=0&plat=6&UUID=846c06d0-1791-4c8e-8882-87d3a79ac496&ext=2097151&c=tv&density=3.0&displayMetrics=1080*2340&encd=g6mEf%2Fw3AWjvgWudW3FoKbxAnS2CnHNhygaYXdKe7vIUDiBNRRV4kD9zIpxwOCDRkjitSQ4E2W%2FdZ17WzpGcIs4J5v2Mk6mDxyDCAYC40uBW%2BHmhbEGNi3Qmn8BJwOXfwnqUTJ68Cnr8qkO2GBiiXUKoDhKVRJ1EAxGZKMReRJYCqRvfIrv%2BbzE59meGl842zqeJPE4h69JmV8v9BOYe8YQHedzabyIMvihPqZ2%2FtrgbWNuduzAgqgqoIs4OqAJp%2BsRsauCSmw7fnLOOiyDGmMxIL9W65Jk5rSNPJ1Rtjatu%2BsYkuGbz7AbLbEKWwQ1oF%2FQNhEkN1g3MWK6WtpX5PAh3otxYMD4ASQvrPNik9EUEXTsMEd6bXPzPH%2BToZyOGxzL18QbTyd4FuU6UjFH6YtAqiyE5WwJJpXrpJR8reNGqHrOlW0y0QnGzfCP6Wm0PGykKfvCxGewqcOwb%2FFQjfM6b0OYoEDWFjb%2F%2BjYUeLIqyvRxk4dEM7zaqQ1OAgdKhXEY%2BghInznpVPXGc45TBWLbJ8UbnE0dEwF1C6h8WXnPVAJtXWEg1rcsxLQ%2BUqtVmNTJxH7S8tvo%2BHo66%2BbdEELxTQHSLOTjBZ%2F%2FRiabHFStMQkzR7Cwkx3DMlSygpMD37tFKpIMb%2F0Xz3K874cyRjAoG9Xfzzar3e%2F7BLVBjwLUlFeTUnd8Rb1wqX21Fiedh9p11Ngux%2BG8yKmJEQfmipqgEkvwDCHbwQDbZTwndfL3m1%2BwHwgzsAHMoLezsHYE5gQWPfh8YfqcwgW4HB565dSAVKUHLMrkh0GGHU9bv0NuYvBGpvbU1KDfWLOSSmOXAE3BQLTLDxkdf7QsaBnoN6eK%2FQC7Zr45OD%2F2zcsTCXFiojYzZ&sver=9.2.20&islocaltv=0&al=9622743&vc=101147;101148&playerScale=0.5625&screenstate=1&poid=1&audited_level=-1&uptime=1772647531&protv=3.0&site=1&partner=93&adoriginal=sohu&build=9.2.20&broadcastID=0&appid=tv&guid=76b516d09e1a54b0df00255ed4103dd4&sdkVersion=tv7.7.10-SNAPSHOT&isroot=false&playerMetrics=1080*607&vu=0"
#     res = GetAdData.get_ad_data(ad_url)
#     data = ET.XML(res.content.decode('utf-8'))
#     cur_el = CompareXml.get_all_elements(data)
#     CompareXml.compare_elements(base_el, cur_el)





