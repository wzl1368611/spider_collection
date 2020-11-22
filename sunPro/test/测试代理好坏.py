#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2020-8-9 23:11:00
# version: 1.0
# __author__: zhilong
import requests
http = ["175.43.151.240:9999",
        '222.94.150.162:3128',
        '123.55.102.203:9999',
        '123.163.115.62:9999',
        '59.62.42.75:9000',
        '1.199.31.156:9999',
        '36.250.156.50:9999',
        '123.163.117.197:9999',
        '123.55.114.42:9999',
        '112.111.217.121:9999',
        '113.194.140.60:9999',
        '113.194.48.139:9999',
        '59.62.41.91:9000',
        '175.42.68.174:9999'
        ]
https = ['49.70.17.204:9999',
         '49.89.87.85:9999',
         '49.70.85.154:9999',
         '49.70.85.53:9999',
         '120.83.121.172:9999',
         '113.195.156.158:9999']
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.111 Safari/537.36 ',

}
for ip in http:
    proxy_ip = f'http://{ip}'
    proxy_dict = {
        'http': proxy_ip,
    }
    try:
        response = requests.get(url='http://www.baidu.com', proxies=proxy_dict, headers=headers)
        if 200 <= response.status_code < 300:
            print(f'-----> ip{ip} 是有效的！')
            with open('effective_ip.txt', 'a') as f:
                f.write('http://'+ip)
    except Exception as e:
        print('-----> 连接超时', e)
for ip in https:
    proxy_ip = f'https://{ip}'
    proxy_dict = {
        'https': proxy_ip,
    }
    try:
        response = requests.get(url='http://www.baidu.com', proxies=proxy_dict, headers=headers)
        if 200 <= response.status_code < 300:
            print(f'-----> ip{ip} 是有效的！')
            with open('effective_ip.txt', 'a') as f:
                f.write('https://'+ip)
    except Exception as e:
        print('-----> 连接超时', e)
# 'http://www.goubanjia.com/'

