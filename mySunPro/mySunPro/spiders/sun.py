# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mySunPro.items import MysunproItem, MyDetailItem


# http://wz.sun0769.com/political/index/politicsNewest
class SunSpider(CrawlSpider):
    name = 'sun'
    # allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&page=']
    link = LinkExtractor(allow=r'id=1&page=\d+')
    link_detail = LinkExtractor(allow=r'id=[0-9]{6}')
    # politics/index?id=482186
    # r'http://wz.sun0769.com/political/index/politicsNewest?id=1&page=\d+'
    # LinkExtractor(allow=r'Items/')
    rules = (
        Rule(link, callback='parse_item', follow=True),
        Rule(link_detail, callback='parse_detail', follow=True),
    )

    def parse_item(self, response):
        item = {}
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        # print(response)
        li_lists = response.xpath('/html/body/div[2]/div[3]/ul[2]//li')
        for li in li_lists:
            new_num = li.xpath('./span[@class="state1"]/text()').extract_first()
            new_title = li.xpath('./span[@class="state3"]/a/text()').extract_first()
            # new_url = li.xpath('./span[@class="state3"]/a/@href').extract_first()
            # http://wz.sun0769.com/political/politics/index?id=482064
            # xpath表达式中不可以出现tbody
            item = MysunproItem()
            item['num'] = new_num
            item['title'] = new_title
            # print(new_num, new_title)
            yield item

    # 解析新闻内容和编号
    def parse_detail(self, response):
        print('获取详情页的结果', response)
        # /html/body/div[3]/div[2]/div[2]/div[1]/span[4]
        new_id = response.xpath('/html/body/div[3]/div[2]/div[2]/div[1]/span[4]/text()').extract_first()
        new_id = response.xpath('//div[@class="focus-date clear focus-date-list"]/span[4]/text()').extract_first()

        # new_content = response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/pre/text()').extract_first()
        new_content = response.xpath('//div[@class="details-box"]/pre/text()').extract_first()
        # /html/body/div[3]/div[2]/div[2]/div[2]/pre
        item = MyDetailItem()
        item['id'] = new_id.split('：')[1]
        item['content'] = new_content
        # print(new_id, new_content)
        yield item
