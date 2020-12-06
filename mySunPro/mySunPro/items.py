# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MysunproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    num = scrapy.Field()
    title = scrapy.Field()


class MyDetailItem(scrapy.Item):
    id = scrapy.Field()
    content = scrapy.Field()
