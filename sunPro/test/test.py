#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2020-8-9 23:11:00
# version: 1.0
# __author__: zhilong
import requests
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 ' \
             'Safari/537.36 '
# url ='http://wz.sun0769.com/political/index/politicsNewest'
url = 'http://www.baidu.com'

http = ["123.179.161.230:41128",
        '171.80.187.163:38367',
        '112.240.182.233:44590',
        '113.226.97.93:55387',
        '117.26.221.137:52067',
        '182.244.168.247:38904',
        '1.199.193.249:35786',
        '183.141.154.179:46691',
        '183.141.154.179:46691',

        ]
# http = ['36.250.156.50:9999']
headers = {
    'user-agent': user_agent
}
for i in http:
    proxy = {
        'http': 'http://%s' % i
    }
    print('代理是：', proxy)
    try:
        response = requests.get(url=url, headers=headers, proxies=proxy)
        print(f'------> {response.status_code}')
        print(response.text)
    except Exception as e:
        print('代理出错了', e)
