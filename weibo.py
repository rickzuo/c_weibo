# !/usr/bin/env python3
# coding：utf-8

import re
import sys
import time
import logging
import datetime
import grequests
from random import choice
from lxml import etree
from requests import Session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from db import Mysql
from settings import WEIBO_URL, USERNAME, PROXIES, TIMEOUT, HEADERS

logger = logging.getLogger(__name__)
today = datetime.datetime.now()


class WeiboComment(object):
    """查看某人在某微博的评论
        weibo_url指微博详情页的地址
        user指所查看用户的昵称
    """

    def __init__(self, weibo_url=WEIBO_URL, user=USERNAME, proxies=PROXIES, timeout=TIMEOUT, headers=HEADERS):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.proxies = proxies
        self.today = f"{today.month}月{today.day}日"
        self.urls = []
        self.timeout = timeout
        self.user = user
        self.weibo_url = weibo_url
        self.cookies = {}
        self.headers = headers

    def _base(self):
        self.driver.get(self.weibo_url)
        time.sleep(5)
        source = self.driver.page_source
        logging.debug(source)
        _cookies = self.driver.get_cookies()
        for cookie in _cookies:
            self.cookies[cookie['name']] = cookie['value']
        self.driver.quit()
        try:
            comments = int(re.findall(r'count="(\d+)"', source)[0])
            if comments % 20 == 0:
                pages = comments // 20
            else:
                pages = comments // 20 + 1
        except IndexError as e:
            logger.error(f"no comments count\n{source}")
            sys.exit(1)
        try:
            weibo_id = re.findall(r'"id=(\d+)&amp;filter', source)[0]
        except IndexError as e:
            logger.error(f"no weibo id\n{source}")
            sys.exit(2)
        self.db = Mysql(weibo_id)
        self.db.create_table(self.weibo_url)
        logger.info(f'总共{pages}页,{comments}评论')
        for page in range(1, pages + 1):
            url = f'https://weibo.com/aj/v6/comment/big?ajwvr=6&id={weibo_id}&filter=all&page={page}'
            self.urls.append(url)

    @staticmethod
    def exception_handler(request, exception):
        logger.error(f"{exception}\n{request.url}")
        return None

    def getcomments(self):
        ss = Session()
        tasks = (grequests.get(url,
                               session=ss,
                               headers=self.headers,
                               cookies=self.cookies,
                               timeout=self.timeout,
                               proxies=choice(self.proxies)
                               ) for url in self.urls)
        bs = grequests.map(tasks,
                           size=5,
                           exception_handler=self.exception_handler,
                           gtimeout=3)
        for b in bs:
            _page = bs.index(b)
            if b:
                _offset = 0
                d = b.json()
                c_html = d['data']['html']
                c = etree.HTML(c_html.encode('unicode_escape'))
                logger.info(f'第{_page + 1}页*********************************************************\n{c_html}')
                uc = c.xpath('//div[@class="WB_text"]')
                dt = c.xpath('//div[@class="WB_from S_txt2"]')
                for i, j in zip(uc, dt):
                    _offset += 1
                    user, comment = i.xpath('string(.)').encode('utf-8').decode('unicode_escape').strip().split('：', 1)
                    c_time = j.xpath('string(.)').encode('utf-8').decode('unicode_escape').strip()
                    if '今天' in c_time:
                        c_time = c_time.replace('今天', self.today)
                    self.db.add(user, comment, c_time, page=_page, offset=_offset)
                    if user == self.user:
                        logger.info(f'{user}:{comment}')
                logger.info(f"该页有{_offset}条评论")

    def run(self):
        self._base()
        self.getcomments()
        self.db.close()
