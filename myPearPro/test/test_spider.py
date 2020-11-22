#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2020-8-9 23:11:00
# version: 1.0
# __author__: zhilong


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Firefox()

driver.get('http://www.python.org')
assert 'Python' in driver.title
elem = driver.find_element_by_name('q')
elem.clear()
elem.send_keys('pycon')
elem.send_keys(Keys.RETURN)
assert 'no results found.' not in driver.page_source
driver.close()





