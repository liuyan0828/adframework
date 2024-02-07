libs:  
CompareXml->对比两个xml的异同  
Config->基础配置文件  
GetAdData->获取广告请求返回值  
GetAdConf->根据广告组id获取mango配置项
CheckResult->校验返回

utils:
LogHandler->日志模块的封装
ReadYaml->读取yaml文件
MakeDir->创建目录
readExpectedResult->读取期望结果文件
RequestsHandler->requests请求封装  
UrlHandler->url处理方式封装  
Xxtea->解密方法  

Script：  
存放测试用例yaml文件，对应的基准json/xml文件   

TestCase：  
存放测试用例，测试模块以test打头，测试类以Test打头，测试方法以test打头  
eg：test_open测试用例，只需修改测试用例yaml文件存放地址即可

Report：  
存放报告

SendAlert.py  
jenkins运行失败发送报警消息

main.py  
执行文件，直接运行main即可。如需运行某个case，指定运行模块或方法即可。