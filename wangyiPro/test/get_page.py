#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2020-8-9 23:11:00
# version: 1.0
# __author__: zhilong

import requests
import random
import re
from lxml import etree
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/86.0.4240.111 Safari/537.36',
}
response = requests.get(url='https://dy.163.com/article/FRVRL3GD051481US.html', headers=headers).text
print(response)
html = etree.HTML(response)
text = html.xpath('//div[@class="post_body"]//p/text()')
print(text)
# with open('hello.html','w') as f:
#     f.write(html)




