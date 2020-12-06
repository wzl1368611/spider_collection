# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from fbsPro.items import FbsproItem

class FbsSpider(RedisCrawlSpider):
    name = 'fbs'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://www.xxx.com/']
    redis_key = 'sun'
    rules = (
        Rule(LinkExtractor(allow=r'id=1&page=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        li_lists = response.xpath('/html/body/div[2]/div[3]/ul[2]//li')
        for li in li_lists:
            new_num = li.xpath('./span[@class="state1"]/text()').extract_first()
            new_title = li.xpath('./span[@class="state3"]/a/text()').extract_first()
            item = FbsproItem()
            item['title'] = new_title
            item['new_num'] = new_num
            yield item
