#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2020-8-9 23:11:00
# version: 1.0
# __author__: zhilong
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import json, re
import requests
import os

chrome_options = Options()
chrome_options.add_argument('--window-size=1500,1366')
driver = webdriver.Chrome(options=chrome_options)

detail_urls = []


def get_video():
    driver.implicitly_wait(10)
    driver.get('https://www.pearvideo.com/category_5')
    time.sleep(5)
    # WebDriverWait(driver, 10).until(By.NAME, '最热')
    # '/html/body/div[2]/h1'
    elements = driver.find_elements_by_xpath('//*[@id="listvideoListUl"]//li')
    nums = len(elements)
    print('-----> {}'.format(nums))
    for i in range(2, 90):  # 也可以设置一个较大的数，一下到底
        js = "var q=document.documentElement.scrollTop={}".format(i * 100)  # javascript语句
        driver.execute_script(js)
    for i in range(1, nums + 1):
        # '//*[@id="listvideoListUl"]/li[1]/div/a/div[2]'
        name = driver.find_element_by_xpath(f'//*[@id="listvideoListUl"]/li[{i}]/div/a/div[2]').text
        # if name=='':
        #     name=driver.find_element_by_xpath('//*[@id="listvideoListUl"]/li[4]/div/a/div[2]')
        obj = driver.find_element_by_xpath(f'//*[@id="listvideoListUl"]/li[{i}]/div/a')
        new_url = obj.get_attribute('href')
        print('-----> 初始的new_url 值：', new_url)
        # new_url = 'https://www.pearvideo.com/'+new_url
        print(f'-----> {name}')
        print(f'-----> {new_url}')
        detail_urls.append(new_url)


def get_video_ok():
    driver.implicitly_wait(10)
    driver.get('https://www.pearvideo.com/category_5')
    time.sleep(5)
    name = driver.find_element_by_xpath('//*[@id="listvideoListUl"]/li[1]/div/a/div[2]').text
    # url = driver.find_element_by_xpath('//*[@id="listvideoListUl"]/li[1]/div/a/@href').text
    print(f'-----> {name}')
    # print(f'-----> {url}')


addrs = []


def get_mp4():
    for i in range(len(detail_urls)):
        driver.get(detail_urls[i])
        time.sleep(7)
        # 获取每一个视频的播放地址，得到mp4文件
        element = driver.find_element_by_xpath('//*[@id="JprismPlayer"]/video')
        addr = element.get_attribute('src')
        print(f'-----> {addr}')
        name = driver.find_element_by_xpath('//*[@id="detailsbd"]/div[1]/div[2]/div/div[1]/h1').text
        print('------ name:', name)
        video = {'name': name, 'addr': addr}
        addrs.append(video)


base_path = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
save_path = os.path.join(base_path, 'video')


# 下载视频
def download_video():
    print('-----> base_path', base_path)
    print('-----> save_path', save_path)
    for i in range(len(addrs)):
        print('-----> 当前下载的视频为：', addrs[i]['name'])
        url = addrs[i]['addr']
        content = requests.get(url).content
        path = os.path.join(save_path, url.split("/")[-1])
        print('-----> 存储的路径为：', path)
        with open(path, 'wb') as f:
            f.write(content)


def main():
    start = time.time()
    get_video()
    get_mp4()
    download_video()
    end = time.time()
    print('-----> 总共花费的时间是：', int(end - start))


if __name__ == '__main__':
    # get_video_ok()
    main()
