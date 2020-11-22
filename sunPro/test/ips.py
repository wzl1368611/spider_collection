#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2020-8-9 23:11:00
# version: 1.0
# __author__: zhilong

import requests
import requests

proxies = {
    "http": "http://111.155.124.78:8123"  # 代理ip
}

headers = {
    "User_Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
}

http_url = "http://www.xicidaili.com/nn/1"
res = requests.get(url=http_url, headers=headers, proxies=proxies, timeout=30)
if res.status_code == 200:
    print("访问网页成功")
else:
    print("代理ip错误")


