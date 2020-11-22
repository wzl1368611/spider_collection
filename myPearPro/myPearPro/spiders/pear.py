# -*- coding: utf-8 -*-
import scrapy
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


class PearSpider(scrapy.Spider):
    name = 'pear'
    allowed_domains = ['pearvideo.com']
    start_urls = ['https://www.pearvideo.com/category_5']
    path = os.path.dirname(os.path.abspath('__file__'))
    download_path = os.path.join(path, 'video')

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1500,1366')
        self.bro = webdriver.Chrome(options=chrome_options,
                                    executable_path='D:\python_charm\爬虫课件\我的项目文件夹\chromedriver.exe')

    def parse(self, response):
        li_lists = response.xpath('//*[@id="listvideoListUl"]/li')
        for li in li_lists:
            title = li.xpath('./div/a/div[2]/text()').extract_first()
            print('-----> 视频的标题是：', title)
            new_url = 'https://www.pearvideo.com/'+li.xpath('./div/a/@href').extract_first()
            print('-----> 视频的详情url是：', new_url)
            yield scrapy.Request(new_url, callback=self.parse_video)
        # video = response.xpath('//*[@id="JprismPlayer"]/video/@src').extract_first()

    # 访问视频详情页，获取video的mp4
    def parse_video(self, response):
        video = response.xpath('//*[@id="JprismPlayer"]/video/@src').extract_first()
        print('-----> video的地址是：', video)
        yield scrapy.Request(video, callback=self.parse_mp4)

    def parse_mp4(self, response):
        name = response.url.split('/')[-1]
        print('-----> 下载的存储的地址1为：',self.path)
        print('-----> 下载的存储的地址2为:', self.download_path)
        with open(os.path.join(self.download_path, name), 'wb') as f:
            f.write(response.body)

    def closed(self, spider):
        self.bro.quit()
