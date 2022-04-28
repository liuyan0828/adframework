"""
-*- coding: utf-8 -*-
@Time : 2021/12/13 
@Author : liuyan
@function : 读取yaml文件
"""
import yaml


class ReadYaml(object):
    def __init__(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        self.content = yaml.load(file_content, yaml.FullLoader)
        print(self.content)

    def GetTestData(self) -> object:
        data = self.content['testcase']
        ids = []
        for i in data:
            ids.append(i['title'])
        return [data, ids]


# if __name__ == '__main__':
#      filename = r'gphone前贴可跳过'
#      r = ReadYaml(filename)
#      print(r.GetTestdata())