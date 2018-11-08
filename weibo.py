# !/usr/bin/env python3
# coding：utf-8

import re
import os
import sys
import time
import pickle
import logging
import datetime
import grequests
import requests
from random import choice
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from db import Mysql
from settings import WEIBO_URL, USERNAME, PROXIES, TIMEOUT, HEADERS, COOKIES, MYSQL

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
        self.proxies = proxies
        self.today = f"{today.month}月{today.day}日"
        self.urls = []
        self.source = ''
        self.timeout = timeout
        self.user = user
        self.weibo_url = weibo_url
        self.cookies = {}
        self.headers = headers

    def get_cookies(self):
        driver = webdriver.Chrome(chrome_options=self.chrome_options)
        driver.get(self.weibo_url)
        time.sleep(5)
        self.source = driver.page_source
        logging.debug(self.source)
        _cookies = driver.get_cookies()
        for cookie in _cookies:
            self.cookies[cookie['name']] = cookie['value']
        with open(COOKIES, 'wb') as f:
            pickle.dump(self.cookies, f)
        driver.quit()

    def _cookies(self):
        if os.path.exists(COOKIES):
            with open(COOKIES, 'rb') as f:
                _cookies = pickle.load(f)
            _res = requests.get(self.weibo_url, cookies=_cookies, headers=self.headers)
            if not _res.history:
                self.cookies.update(_cookies)
                self.source = _res.text
                logging.info(self.source)
            else:
                self.get_cookies()
        else:
            self.get_cookies()

    def _base(self):
        try:
            comments = int(re.findall(r'count=\\"(\d+)', self.source)[0])
            if comments % 20 == 0:
                pages = comments // 20
            else:
                pages = comments // 20 + 1
        except IndexError:
            logger.error(f"no comments count\n{self.source}")
            sys.exit(1)
        try:
            weibo_id = re.findall(r'%3D(\d+)&title', self.source)[0]
            logging.info(f"Weibo_id:{weibo_id}")
        except IndexError as e:
            logger.error(f"no weibo id\n{self.source}")
            sys.exit(2)
        if MYSQL:
            self.db = Mysql(weibo_id)
            self.db.create_table(self.weibo_url)
        logger.info(f'总共{pages}页,{comments}评论')
        for page in range(1, pages + 1):
            url = f'https://www.weibo.com/aj/v6/comment/big?ajwvr=6&id={weibo_id}&filter=all&page={page}'
            self.urls.append(url)

    @staticmethod
    def exception_handler(request, exception):
        logger.error(f"{exception}\n{request.url}")
        return None

    def getcomments(self, urls=None):
        if urls:
            self.urls = urls
        ss = requests.Session()
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
            if not b:
                continue
            if b.status_code == 200:
                logger.info(f"{b.url} --- {b.status_code}")
                _offset = 0
                d = b.json()
                c_html = d['data']['html']
                c = etree.HTML(c_html.encode('unicode_escape'))
                logger.info(f'第{_page + 1}页')
                logger.debug(f'{c_html}')
                uc = c.xpath('//div[@class="WB_text"]')
                dt = c.xpath('//div[@class="WB_from S_txt2"]')
                for i, j in zip(uc, dt):
                    _offset += 1
                    user, comment = i.xpath('string(.)').encode('utf-8').decode('unicode_escape').strip().split('：', 1)
                    c_time = j.xpath('string(.)').encode('utf-8').decode('unicode_escape').strip()
                    if '今天' in c_time:
                        c_time = c_time.replace('今天', self.today)
                    if MYSQL:
                        self.db.add(user, comment, c_time, page=_page, offset=_offset)
                    if user == self.user:
                        logger.info(f'{user}:{comment}')
                logger.info(f"该页有{_offset}条评论")
            else:
                logger.error(f"{b.url} --- {b.status_code}")

    def run(self):
        self._cookies()
        self._base()
        self.getcomments()
        if MYSQL:
            self.db.close()
