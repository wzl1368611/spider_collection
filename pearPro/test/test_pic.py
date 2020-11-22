#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2020-8-9 23:11:00
# version: 1.0
# __author__: zhilong

import requests
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.111 Safari/537.36 '

}

url = "https://image1.pearvideo.com/cont/20201117/11724129-171259-1.png"
pic_name = url.split('/')[-1]
print('------>', pic_name)
content = requests.get(url, headers=headers).content
with open('../imgs/{}'.format(pic_name), 'wb') as f:
    f.write(content)
