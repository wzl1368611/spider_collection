#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2020-8-9 23:11:00
# version: 1.0
# __author__: zhilong

from scrapy.selector import Selector
import requests
import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root',
                       password='rootpwd', port=3306, database='spider')

cursor = conn.cursor()


def crawl_ips():
    """
    爬取快代理的所有ip port speed proxy_type,并存储到数据库spider的proxy_ip表中
    :return:Nothing
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    for i in range(1, 3576):
        # 'http://h.zhimaruanjian.com/?utm-source=zmrj&utm-keyword=?zmrj888'
        url = 'https://www.kuaidaili.com/free/inha/%d' % i

        re = requests.get(url, headers=headers)
        selector = Selector(text=re.text)
        all_trs = selector.css('.table.table-bordered.table-striped tbody tr')
        ip_list = []
        for tr in all_trs[0:]:
            speed_str = tr.css('td::text').extract()[5]
            print(speed_str, '-----------------------')
            if speed_str:
                speed = float(speed_str.split('秒')[0])
            all_texts = tr.css('td::text').extract()
            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[3]
            # attrvalue = tr.css('td::attr(data-title)').extract()
            # print(attrvalue, '++++++++++++')
            print(ip, port, proxy_type, sep=' ')
            ip_list.append((ip, port, speed, proxy_type))

        for ip_info in ip_list:
            cursor.execute('''insert into proxy_ip(ip,port,speed,proxy_type) 
            values ("{0}","{1}",{2},"{3}")'''.format(ip_info[0], ip_info[1], ip_info[2], ip_info[3]))
            conn.commit()
            # cursor.close()
            # conn.close()


class GetIP(object):
    """
    从数据库表中取出所有的ip和port，
    判断表中的ip代理是否有效，如无效则删除，如有效，则保留
    """

    def delete_ip(self, ip):
        delete_sql = '''delete from proxy_ip 
        where ip="{0}"'''.format(ip)
        print('-----> 删除的ip:', ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        http_url = 'http://www.baidu.com'
        proxy_url = 'http://{0}:{1}'.format(ip, port)
        proxy_dict = {
            'http': proxy_url,
        }
        try:
            response = requests.get(http_url, proxies=proxy_dict, timeout=8)
            # print(response.status_code)
        except Exception as e:
            print('invalid ip and port!')  # 无效的ip port提示
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if 200 <= code < 300:
                print('effective ip!')  # 输出提示为有效的ip 端口
                return True
            else:
                print('invalid ip and port!')  # 输出提示为无效ip 端口

                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # random_sql = '''
        # SELECT ip,port FROM proxy_ip
        # ORDER BY id ASC LIMIT 682
        # '''
        random_sql = '''SELECT ip,port FROM proxy_ip'''
        result = cursor.execute(random_sql)
        # print('待测试的ip的总数是：', len(cursor.fetchall()))
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            print(ip, port, '=======================')
            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return 'http://{0}:{1}'.format(ip, port)
            else:
                return self.get_random_ip()


total = 0


def get_num():
    sql = 'select count(*) from proxy_ip'
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    # cursor.close()
    print('-----> 数据库中的ip的总数是：', result)
    return result


# print(crawl_ips())
if __name__ == '__main__':
    get_ip = GetIP()
    get_ip.get_random_ip()
    # crawl_ips()
    # get_num()
