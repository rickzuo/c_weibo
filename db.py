# !/usr/bin/env python3
# coding:utf-8

import pymysql


class Mysql(object):
    """for mysql"""

    def __init__(self, weibo_id):
        self.con = pymysql.connect(user='root', password='622729', db='weibo')
        self.cursor = self.con.cursor()
        self.t_name = f"w{weibo_id}"

    def create_table(self):
        sql = f"CREATE TABLE `{self.t_name}` (`id` int(10) NOT NULL AUTO_INCREMENT," \
              f"`name` varchar(30),`comment` varchar(1000),PRIMARY KEY (`id`))"
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(f"failed to create table {self.t_name} with excption {e}")

    def add(self, name, comment):
        sql = f"INSERT INTO `{self.t_name}` (`name`, `comment`) VALUES ({name}, {comment})"
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(f"{sql}")

    def close(self):
        self.cursor.close()
        self.con.close()
