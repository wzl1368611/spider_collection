## spider_collection

爬虫合集

---
* myPearPro
### 本项目中介绍
1. 使用了selenium，需要添加匹配的chromedriver.exe的路径在webdriver.Chrome(executable_path='path')
2. 请求视频详情页 如：https://www.pearvideo.com/video_1708124 , xpath 解析、获取其下的.mp4播放地址时，需要用slelenium动态加载
3. 下载了https://www.pearvideo.com/category_5 板块中 生活：LIFE 下的 最热 中的四个视频
4. mp4播放地址url 类似：https://video.pearvideo.com/mp4/third/20201120/cont-1708124-15454898-191438-hd.mp4
5. 访问视频详情页，获取video的mp4文件的url,然后下载到本地目录当中
---
* pearPro
### 本项目中介绍
1. 使用了selenium，需要添加匹配的chromedriver.exe的路径在webdriver.Chrome(executable_path='path')
2. 请求视频详情页 如：https://www.pearvideo.com/video_1708124 , xpath 解析、获取其下的.mp4播放地址时，需要用slelenium动态加载
3. 下载了https://www.pearvideo.com/category_5 板块中 生活：LIFE 下的 最热 中的四个视频
4. mp4播放地址url 类似：https://video.pearvideo.com/mp4/third/20201120/cont-1708124-15454898-191438-hd.mp4
5. 访问视频详情页，获取video的mp4文件的url,然后下载到本地目录当中
---
* sunPro
### 本项目中运用了相关技术
1. fake_useragent的随机ua
2. http://www.goubanjia.com/中的动态代理ip
3. time.sleep(delay)随机延迟数，来降低被反爬虫策略监控的风险
4. 存储数据在mysql数据库中
5. 经本人测试，可爬取阳光政务的 http://wz.sun0769.com/political/index/politicsNewest 中2000页数据，爬取全部网页不在话下
---
* wangyiPro
### 本项目简单介绍
1. 爬取网易中的五大板块新闻：国内、国际、军事、航空、无人机
2. 初始url是：https://news.163.com/，板块url类似：https://news.163.com/domestic/
3. 从初始url获取各个板块url地址，然后获得板块中系列新闻的标题 title 和详情 url，最后访问详情 url 取得新闻的 content
3. 特别注意五大板块的不同类型、题材的新闻，其详情页面的解析各不相同，需要区分对待，用 xpath 解析出内容 content
4. 设置了 selenium 来爬取异步加载的内容
5. 设置了 js 代码来控制浏览器滑块滑动，获取更多动态加载的板块中 url
---
