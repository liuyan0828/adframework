libs:  
CompareXml->对比两个xml的异同  
Config->基础配置文件  
GetAdData->获取广告请求返回值  
RequestsHandler->requests请求封装  
UrlHandler->url处理方式封装  
Xxtea->解密方法  

Yaml：  
存放测试用例yaml文件，按格式填写即可  
ReadYaml->读取yaml文件  

TestCase：  
存放测试用例，测试模块以test打头，测试类以Test打头，测试方法以test打头  
eg：test_gphone测试用例，只需修改测试用例yaml文件存放地址即可

基准xml：  
存放基准xml文件  

main.py  
执行文件，直接运行main即可。如需运行某个case，指定运行模块或方法即可。