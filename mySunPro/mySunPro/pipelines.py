# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class MysunproPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', passwd='rootpwd', db='sun', charset='utf8mb4')
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        # 判断item的类型
        # 将数据写入数据库时，如何保证数据的一致性，id和num相等
        if item.__class__.__name__ =='MyDetailItem':
            print('-----> 来自于详情页')
            print(item['id'], item['content'])
            # 想数据库表中写入数据
            # sql = 'insert into sun2(num,content) values ("%s","%s")' % (item['id'], item['content'])
            sql = 'update sun2 set content="{0}" where num={1}'.format(item['content'], item['id'])

            print('-----> sql语句是：', sql)
            self.cursor.execute(sql)
            self.conn.commit()
        else:
            # 向数据库表中写入数据
            print('-----> 来自于列表页')
            print(item['num'], item['title'])
            # sql = 'insert into sun2(title) values ("%s") where num = %s ' % (item['title'], item['num'])
            sql = 'insert into sun2(num,title) values ("%s","%s")' % (item['num'], item['title'])

            print('-----> sql语句是：', sql)
            self.cursor.execute(sql)
            self.conn.commit()

        return item
