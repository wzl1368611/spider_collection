# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time
from scrapy import signals
from fake_useragent import UserAgent
import requests

class MysunproSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MysunproDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.ua = UserAgent(verify_ssl=False)
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.ua.random
        delay = random.randint(0, 3)
        time.sleep(delay)
        # 动态代理ip,此处为api接口url,访问可动态返回代理ip
        apiUrl = 'http://api.goubanjia.com/dynamic/get/9ec90437c17a332fb83067f5cb7539e4.html?sep=3'
        # 'http://api.goubanjia.com/dynamic/get/9ec90437c17a332fb83067f5cb7539e4.html?sep=3'
        # 要抓取的目标网站地址 ,本人使用的为http://www.goubanjia.com/站的代理ip(全网代理ip)
        # targetUrl = "http://1212.ip138.com/ic.asp";
        # 获取IP列表
        res = requests.get(apiUrl).text.strip("\n")
        # 按照\n分割获取到的IP
        ips = res.split("\n")
        # 随机选择一个IP
        proxy_ip = random.choice(ips)

        # 利用动态加载的代理ip，设置url的proxy
        if request.url.startswith("http://"):
            request.meta['proxy'] = "http://%s" % proxy_ip  # http代理
        elif request.url.startswith("https://"):
            request.meta['proxy'] = "https://%s" % proxy_ip  # https代理
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
