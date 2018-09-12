# !/usr/bin/env python3
# coding:utf-8

import pymysql
import logging
from settings import HOST, USER, PASSWORD, DB

logger = logging.getLogger('weibo')


class Mysql(object):
    """for mysql"""

    def __init__(self, weibo_id):
        self.con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8mb4')
        self.cursor = self.con.cursor()
        self.t_name = f"w{weibo_id}"

    def create_table(self):
        sql = f"CREATE TABLE `{self.t_name}` (`id` int(10) NOT NULL AUTO_INCREMENT," \
              f"`name` varchar(30),`comment` varchar(1000),PRIMARY KEY (`id`),INDEX (name)) DEFAULT CHARSET=utf8mb4"
        try:
            self.cursor.execute(sql)
        except Exception as e:
            logger.error(f"failed to create table {self.t_name} with exception {e}")

    def add(self, name, comment):
        sql = f"INSERT INTO `{self.t_name}` (`name`, `comment`) VALUES ('{name}', '{comment}')"
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as e:
            logger.error(f"{sql}\n{e}")

    def close(self):
        self.cursor.close()
        self.con.close()
