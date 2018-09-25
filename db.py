# !/usr/bin/env python3
# coding:utf-8

import pymysql
import logging
from settings import HOST, USER, PASSWORD, DB

logger = logging.getLogger(__name__)


class Mysql(object):
    """for mysql"""

    def __init__(self, weibo_id):
        self.con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8mb4', write_timeout=2)
        self.t_name = f"w{weibo_id}"

    def create_table(self, url=None):
        sql = f"CREATE TABLE `{self.t_name}` (`id` int(10) NOT NULL AUTO_INCREMENT," \
              f"`name` varchar(30),`comment` varchar(1000),`time` varchar(20),PRIMARY KEY (`id`),INDEX (name)) " \
              f"DEFAULT CHARSET=utf8mb4 COMMENT='{url}'"
        # noinspection PyBroadException
        try:
            with self.con.cursor() as cursor:
                cursor.execute(sql)
        except Exception as e:
            logger.warning(f"failed to create table {self.t_name} with exception {e}")
        self.con.commit()

    def add(self, name, comment, c_time, page, offset):
        _comment = pymysql.escape_string(comment)
        sql = f'INSERT INTO `{self.t_name}` (`name`, `comment`, `time`) VALUES ("{name}", "{_comment}", "{c_time}")'
        logger.debug(f'{page * 20 + offset}----------{name}:{_comment}-----{c_time}')
        # noinspection PyBroadException
        try:
            with self.con.cursor() as cursor:
                cursor.execute(sql)
        except Exception as e:
            logger.error(f"{sql}\n{e}")
        self.con.commit()

    def close(self):
        self.con.close()
