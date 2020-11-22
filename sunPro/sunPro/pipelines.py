# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exceptions import DropItem
import xlrd
import xlwt
import xlutils

from xlutils.copy import copy


class SunproPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['sid'] in self.ids_seen:
            raise DropItem('Duplicate item found: %s' % item)
        else:
            self.ids_seen.add(item['sid'])
        # 处理得到的数据
        # 1.写入数据库中
        # 2.保存到表格中
        print(item)

        return item
        # index = len(value)  # 获取需要写入数据的行数
        '''
        try:
            workbook = xlrd.open_workbook('详情.xls')  # 打开工作簿
            sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
            if len(sheets) == 0:
                sheet = workbook.add_sheet('相关信息')
            else:
                worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
            rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
            new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
            new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
            value = list(item.values())
            for i in len(value):
                new_worksheet.write(rows_old, i, value[i])  # 追加写入数据，注意是从i+rows_old行开始写入
            new_workbook.save('详情.xls')  # 保存工作簿
            print("xls格式表格【追加】写入数据成功！")
        except Exception as e:
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet('相关信息')
            # 表格的头
            for i in range(len(item.keys())):
                sheet.write(0, i, list(item.keys())[i])
            # 写入数据
            for i in range(len(item.values())):
                sheet.write(1, i, list(item.values())[i])
            workbook.save('详情.xls')

        return item
        '''


class mysqlPipeline(object):
    def __init__(self):
        # self.ids_seen = set()
        self.db = pymysql.connect(
            host='localhost',  # 连接的是本地数据库
            user='root',  # 自己的mysql用户名
            passwd='rootpwd',  # 自己的密码
            db='sun',  # 数据库的名字
            charset='utf8mb4',  # 默认的编码方式：
            cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        '''
        :param item: 对象
        :param spider: 爬虫
        :return:
        '''
        # if item['sid'] in self.ids_seen:
        #     raise DropItem('Duplicate item found: %s' % item)
        # else:
        #     self.ids_seen.add(item['sid'])
        # 将爬取的信息保存到mysql
        # 将item里的数据拿出来
        # title = item['title']
        # link = item['link']
        # posttime = item['posttime']

        sid = int(item["sid"])
        status = item["status"]
        title = item["title"]
        rep_time = item["rep_time"]
        ask_time = item["ask_time"]
        content = item['content']
        department = item['department']

        # 和本地的newsDB数据库建立连接

        try:
            # 使用cursor()方法获取操作游标
            # cursor = self.db.cursor()
            # SQL 插入语句
            sql = "INSERT INTO sun(sid,status,title,content,department ,ask_time,rep_time) \
                  VALUES (%d,'%s','%s','%s', '%s', '%s','%s')" % (sid, status, title, content, department, ask_time, rep_time)
            # 执行SQL语句
            print('-----> sql语句是：', sql)
            self.cursor.execute(sql)
            # 提交修改
            self.db.commit()
        except Exception as e:
            print('-----> 存储数据出错了', e)
            # 关闭连接
            self.db.close()
            self.cursor.close()

        return item

    def close_spider(self, spider):
        pass
