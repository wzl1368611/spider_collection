# -*- coding: utf-8 -*-
import scrapy
import os
import random
# 当前的路径为：
# base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_path)
import sys
import logging

from sunPro.items import SunproItem


# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('__file__'))))

class SunSpider(scrapy.Spider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest', ]
    # start_urls = ['http://wz.sun0769.com/political/index/politicsNewest',
    #               'http://wz.sun0769.com/political/index/politicsNewest?id=1&page=2',
    #               'http://wz.sun0769.com/political/index/politicsNewest?id=1&page=3',
    #               'http://wz.sun0769.com/political/index/politicsNewest?id=1&page=4',
    #               'http://wz.sun0769.com/political/index/politicsNewest?id=1&page=5']

    # 翻页的url
    page_urls = []

    # http://wz.sun0769.com/political/index/politicsNewest?id=1&page=2

    # 下一页 <a href="/political/index/politicsNewest?id=1&amp;page=3" class="arrow-page prov_rota"></a>
    def parse(self, response):
        # 获取解析页面

        # for i in range(1, 3):
        #     page = i+1
        #     print('-----> 目前的页数为：', page)
        #     yield scrapy.Request(f'http://wz.sun0769.com/political/index/politicsNewest?id=1&page={page}',
        #                          callback=self.parse)

        # if 200 <= response.status <= 300:

        # new_urls = 'http://wz.sun0769.com' + response.xpath('//div[@class="mr-three paging-box"]/a[2]/@href').extract_first()
        # print('-----> 新得页面的url是：', new_urls)
        # if new_urls:
        #     self.page_urls.append(new_urls)
        for page in range(1, 1000):
            url = 'http://wz.sun0769.com/political/index/politicsNewest?id=1&page=%d' % page
            print('------> url', url)
            yield scrapy.Request(url=url, callback=self.parse_item)
        # logging.info('当前访问的url是 %s' % response.url)

        # 此处为翻页
        # new_urls = []
        # try:
        #     new_urls = response.xpath('/html/body/div[2]/div[3]/div[3]/div//a/@href').extract()
        #     # '/html/body/div[2]/div[3]/div[3]/div/a[2]'
        #     print('-----> 新的url列表为：', new_urls)
        # except Exception as e:
        #     print('解析下一页标签出错了 | 已经是最后一页，没有下一页标签了', e)
        # if len(new_urls) > 0:
        #     for i in range(len(new_urls)):
        #         page_url = new_urls[i]
        #         print('-----> page_url', page_url)
        #         yield scrapy.Request('http://wz.sun0769.com' + page_url, callback=self.parse)

        # 'http://wz.sun0769.com/political/index/politicsNewest?id=1&page=1'
        # for url in response.xpath('/html/body/div[2]/div[3]/div[3]/div//a/@href').extract():
        #     print('-----> 每一条url是', url)
        #     yield scrapy.Request('http://wz.sun0769.com'+url, callback=self.parse)

        # 得出下一页的标签，进行翻页操作，并且拼接成url访问

    def parse_item(self, response):
        if 200 <= response.status <=300:
            print('-----> 当前正在解析的页面为：', response.url)
            li_lists = response.xpath('/html/body/div[2]/div[3]/ul[2]//li')
            for li in li_lists:
                item = SunproItem()
                sid = li.xpath('./span[1]/text()').extract_first()
                status = li.xpath('./span[2]/text()').extract_first()
                ask_title = li.xpath('./span[3]/a/text()').extract_first()
                rep_time = li.xpath('./span[4]/text()').extract_first()
                ask_time = li.xpath('./span[5]/text()').extract_first()


                item["sid"] = sid
                item["status"] = status
                item["title"] = ask_title
                item["rep_time"] = rep_time
                item["ask_time"] = ask_time
                print('-----> 编号：', sid)
                print('-----> 状态：', status)
                print('-----> 问政标题：', ask_title)
                print('-----> 问政时间：', ask_time)
                print('-----> 回复时间：', rep_time)
                # 查找详情
                detail_url = 'http://wz.sun0769.com' + li.xpath('./span[3]/a/@href').extract_first()
                print('-----> 详情内容的url是：', detail_url)
                yield scrapy.Request(url=detail_url, meta={'item': item},
                                     callback=self.parse_detail)
        else:
            print('-----> 错误的status代码是', response.status)

    def parse_detail(self, response):
        item = response.meta['item']
        details = response.xpath('//div[@class="details-box"]/pre/text()').extract_first()
        content = ''.join(details)
        if content == '':
            content = '未知'
        print('-----> 详情内容是：', content)
        # 问政主体 ： 部门是--
        department = response.xpath('//div[@class="mr-three clear"]/div[@class="fl politics-fl"]/text()').extract_first()
        # '/html/body/div[3]/div[2]/div[2]/div[3]/div[1]'
        department = department.split(':')[-1]
        print('-----> 问政部门是：', department)
        if department == '':
            department = '未知'
        item['content'] = content
        item['department'] = department
        yield item
