#!/usr/bin/env python
# coding: utf-8

# In[33]:


import json, requests

weatherJsonUrl = "http://wthrcdn.etouch.cn/weather_mini?city=北京"  # 将链接定义为一个字符串
response = requests.get(weatherJsonUrl)  # 获取并下载页面，其内容会保存在respons.text成员变量里面
response.raise_for_status()  # 这句代码的意思如果请求失败的话就会抛出异常，请求正常就上面也不会做

# 将json文件格式导入成python的格式
weatherData = json.loads(response.text)
#pprint.pprint(weatherData)

'''weather_dict = dict()
weather_dict['high'] = weatherData['data']['forecast'][0]['high']
weather_dict['low'] = weatherData['data']['forecast'][0]['low']
weather_dict['type'] = weatherData['data']['forecast'][0]['type']
weather_dict['fengxiang'] = weatherData['data']['forecast'][0]['fengxiang']
weather_dict['ganmao'] = weatherData['data']['ganmao']
print(weather_dict['high'])
pprint.pprint(weather_dict['high'],weather_dict['low'],weather_dict['type'],weather_dict['fengxiang'],weather_dict['ganmao'])'''
#print(weather_dict)
weather_json = ""
weather_json += str(weatherData['data']['forecast'][0]['high'])+"   "
weather_json += str(weatherData['data']['forecast'][0]['low'])+"   "
weather_json += str(weatherData['data']['forecast'][0]['type'])+"   "
weather_json += str(weatherData['data']['forecast'][0]['fengxiang'])+"   "
print(weather_json)
suggest = str(weatherData['data']['ganmao'])
print(suggest)


# In[ ]:




