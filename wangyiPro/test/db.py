#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2020-8-9 23:11:00
# version: 1.0
# __author__: zhilong
import pymysql


def init():
    conn = pymysql.connect(host='localhost', user='root', password='rootpwd', charset='utf8mb4', db='spider')
    cursor = conn.cursor()
    sql = '''
    create table wangyi(id int primary key auto_increment,
    title varchar(256),
    content text)
    '''
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def main():
    pass


if __name__ == '__main__':
    init()
