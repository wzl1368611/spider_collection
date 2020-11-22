# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from wangyiPro.items import WangyiproItem


class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    allowed_domains = ['news.163.com']
    start_urls = ['https://news.163.com/']
    model_urls = []

    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='D:\python_charm\爬虫课件\我的项目文件夹\chromedriver.exe')

    # 解析五大板块详情Url
    def parse(self, response):
        li_lists = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        lists = [3, 4, 6, 7, 8]
        themes = []
        for li in li_lists:
            theme = li.xpath('./a/@href').extract_first()
            print('-----> 每一个板块的分别是：', theme)
            themes.append(theme)
        for i in lists:
            model_url = themes[i]
            print('-----> 请求的主题分别是', model_url)
            self.model_urls.append(model_url)
        for req_url in self.model_urls:
            yield scrapy.Request(req_url, callback=self.parse_model)

    def parse_model(self, response):  # 解析每一个板块页面中对应新闻的标题和详情页的url
        div_lists = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_lists:
            item = WangyiproItem()
            title = div.xpath('./div[1]/div[1]/h3/a/text()').extract_first()
            item['title'] = title
            print('------> 标题是：', title)
            new_detail_url = div.xpath('./div[1]/div[1]/h3/a/@href').extract_first()
            if new_detail_url:
                # 对新闻详情页的url发起请求
                print('-----> 详情url是：', new_detail_url)
                yield scrapy.Request(url=new_detail_url, meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):  # 用于解析新闻内容

        #  特别注意五大板块的内容url 的解析放不相同，来自不同板块的内容的url的content的xpath解析是不同的
        # 要分别解析


        print('============================== 获取的页面为：', response.url)
        # print(response.text)
        item = response.meta['item']
        contents = response.xpath('//*[@id="endText"]//p/text()').extract()
        if len(contents) == 0:
            contents = response.xpath('//*[@id="content"]/div[2]//p/text()').extract()
        # '//*[@id="endText"]//p/text()'
        # '//*[@id="content"]/div[2]'
        # '//*[@id="content"]/div[2]'
        # '//*[@id="content"]/div[2]'
        # '//*[@id="content"]/div[2]'
        contents = ''.join(contents)
        print('-----> 内容是：', contents)
        item['content'] = contents
        yield item

    # 爬虫结束关闭浏览器
    def closed(self, spider):
        self.bro.quit()
