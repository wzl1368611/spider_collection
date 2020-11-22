# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SunproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sid = scrapy.Field()     # 编号
    status = scrapy.Field()     # 状态
    title = scrapy.Field()  # 问政标题
    rep_time = scrapy.Field()   # 回复时间
    ask_time = scrapy.Field()   # 问政时间
    content = scrapy.Field()    # 问政内容
    department = scrapy.Field()  # 问政主体
