# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class WangyiproPipeline:
    def __init__(self):
        pass

    def process_item(self, item, spider):
        # print(item)
        conn = pymysql.connect(host='localhost', user='root', password='rootpwd', db="spider", charset='utf8mb4')
        cursor = conn.cursor()
        try:
            sql = 'insert into wangyi(title,content) values ("%s","%s")' % (item['title'], item['content'])
            print('-----> sql语句是：', sql)
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print('-----> 保存到数据库时报错', e)
        finally:
            conn.close()
            cursor.close()

        return item

