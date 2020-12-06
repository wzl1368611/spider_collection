# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time
import urllib3
from scrapy import signals
import requests
import random
from fake_useragent import UserAgent


class SunproSpiderMiddleware:
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


# http = ["123.179.161.230:41128",
#         '171.80.187.163:38367',
#         '112.240.182.233:44590',
#         '113.226.97.93:55387',
#         '117.26.221.137:52067',
#         '182.244.168.247:38904',
#         '1.199.193.249:35786',
#         '183.141.154.179:46691',
#         '183.141.154.179:46691',
#         ]


# https = ['49.70.17.204:9999',
#          '49.89.87.85:9999',
#          '49.70.85.154:9999',
#          '49.70.85.53:9999',
#          '120.83.121.172:9999',
#          '113.195.156.158:9999']

class SunproDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        '''
        self.user_agent_list = [
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) '
            'Chrome/10.0.648.133 Safari/534.16',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36)'
        ]
        '''

        # 随机ua改为fake_useragent比较有派头，方便获取，实时更新
        self.ua = UserAgent(verify_ssl=False)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # 下载中间件 改变发出的请求
    def process_request(self, request, spider):
        # 设置随机ua
        # request.headers['User-Agent'] = random.choice(self.user_agent_list)
        request.headers['User-Agent'] = self.ua.random

        # 设置time.sleep随机延迟 降低爬取速率，防止被封ip
        delay = random.randint(0, 3)
        time.sleep(delay)

        # 动态代理ip,此处为api接口url,访问可动态返回代理ip
        apiUrl = 'http://api.goubanjia.com/dynamic/get/9ec90437c17a332fb83067f5cb7539e4.html?sep=3'
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
