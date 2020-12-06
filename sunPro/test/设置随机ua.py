#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2020-8-9 23:11:00
# version: 1.0
# __author__: zhilong
from fake_useragent import UserAgent

# faker_useragent的使用
ua = UserAgent(verify_ssl=False)
custom_ua = ua.random
chrome_ua = ua.chrome
# another = ua.data_randomize
print('-----> 随机ua是:', custom_ua)
print('-----> chrome_ua是:', chrome_ua)
