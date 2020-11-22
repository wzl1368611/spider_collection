# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import os


class PearSpider(scrapy.Spider):
    name = 'pear'
    allowed_domains = ['www.pearvideo.com']
    start_urls = ['https://www.pearvideo.com/category_5']

    def parse(self, response):
        li_lists = response.xpath('//*[@id="listvideoListUl"]//li')
        for li in li_lists:
            title = li.xpath('./div/a/div[2]/text()').extract_first()
            new_url = 'https://www.pearvideo.com/' + li.xpath('./div/a/@href').extract_first()
            time = li.xpath('./div/a/div/div[2]/text()').extract_first()
            pic = li.xpath('./div/a/div/div/div/@style').extract_first()
            pic_url = re.findall(r'url(.*?);', pic)[0].replace('(', '').replace(')', '')

            print('----->', pic_url)
            print('----->', title)
            print('-----> 视频详情的url', new_url)
            print('----->', time)
            parse_pic(pic_url)
            scrapy.Request(url=new_url, callback=self.parse_detail)

    # 获得视频地址的url
    def parse_detail(self, response):
        # '//*[@id="JprismPlayer"]/video'
        text = response.xpath('//*[@id="JprismPlayer"]/video').extract_first()
        dates = response.xpath('//*[@id="1707108"]/a/div[1]/img/@src').extract_first()
        print(f'-----> {dates}')
        pattern = re.compile('cont/(.*?)/cont')
        new_dates = pattern.findall(dates)[0]
        print(f'-----> {new_dates}')
        '''
        #先解析获取到的网页源码
        html = etree.HTML(response)
        #获取script的内容，获得的结果是str类型
        data = html.xpath('//script[@class="xxxx"]\text()')[0]
        #或者 data = html.xpath('//script[@id="xxxx"]\text()')[0]
        #再次对获取到的html内容进行解析
        data_html = etree.HTML(data)
        #ok ,现在可以对内容进行xpath匹配了
        '''
        # 获取script标签下的内容
        contId = response.xpath('/html/body/script[2]/@contId').extract_first()
        postUserId = response.xpath('/html/body/script[2]/@postUserId').extract_first()
        before_hd = ''
        # 如何获取111507的数据
        # 访问异步js，解析得到部分视频Url的内容，然后通过解析得到具体url内容
        # ’https://www.pearvideo.com/videoStatus.jsp?contId=1707983&mrd=0.819575158722347‘





        # 梨视频得出视频地址的url
        # 'https://www.pearvideo.com/videoStatus.jsp?contId=1707983&mrd=0.819575158722347'
        # 'https://video.pearvideo.com/mp4/third/20201120/1605873866672-11005350-111508-hd.mp4'

        # '<script type="text/javascript">
        # var isLogin = "false",isFavorited = "0",contId = "1707224",commentLoad = false,contLoad = true,nPageidx = "";
        # var hotcommIds = "23235031,",postId = "1667919",myinfoId = "",postUserId = "15591790",localStorageName = "localVideoKeys",localScrollTop = "VideocrollTop",localtimestamp = "Videotimestamp",shareType = 1;//垂直详情页分享
        # </script>'
        #  https://video.pearvideo.com/mp4/third/20201116/cont-1707224-15591790-154221-hd.mp4

        # div class="video-main">
        #       <img class="img" src="https://image1.pearvideo.com/cont/20201116/cont-1707108-12508264.jpg" alt="航拍：好客山东，魅力青岛！">
        #                                      <div class="vdo-time">02:44</div></div>
        # https://video.pearvideo.com/mp4/third/20201120/cont-1707983-11005350-111508-hd.mp4
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.111 Safari/537.36',
}

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def parse_pic(pic_url):
    # 存储图片的函数
    pic_name = pic_url.split('/')[-1]
    print('----->', pic_name)
    # path = os.path.join(base_path, pic_name)
    # print('----->', path)
    content = requests.get(pic_url, headers=headers).content
    with open('{}/imgs/{}'.format(base_path, pic_name), 'wb') as f:
        f.write(content)
        print('-----> 下载图片成功')
