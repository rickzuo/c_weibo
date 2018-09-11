# !/usr/bin/env python3
# coding：utf-8

import time
import re
import grequests
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from db import Mysql


class WeiboComment(object):
    def __init__(self, weibo_url,  user):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.urls = []
        self.user = user
        self.weibo_url = weibo_url
        self.cookies = {}
        self.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/57.0.2987.133 Safari/537.36",
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }

    def _base(self):
        self.driver.get(self.weibo_url)
        time.sleep(5)
        source = self.driver.page_source
        _cookies = self.driver.get_cookies()
        for cookie in _cookies:
            self.cookies[cookie['name']] = cookie['value']
        self.driver.close()
        comments = int(re.findall(r'<em>(\d+)<', source)[0])
        if comments % 20 == 0:
            pages = comments//20
        else:
            pages = comments//20 + 1
        weibo_id = re.findall(r'"id=(\d+)&amp;filter', source)[0]
        self.db = Mysql(weibo_id)
        self.db.create_table()
        print(f'总共{pages}页,{comments}评论')
        for page in range(1, pages+1):
            url = f'https://weibo.com/aj/v6/comment/big?ajwvr=6&id={weibo_id}&filter=all&page={page}'
            self.urls.append(url)

    @staticmethod
    def exception_handler(request, exception):
        try:
            return requests.get(request.url, headers=request.headers, cookies=request._cookies)
        except Exception as e:
            print(f"{exception}\n{request.url}\n{e}")

    def getcomments(self):
        tasks = (grequests.get(url, headers=self.headers, cookies=self.cookies) for url in self.urls)
        bs = grequests.map(tasks, size=10, exception_handler=self.exception_handler)
        for b in bs:
            if b:
                d = b.json()
                c_html = d['data']['html']
                c = etree.HTML(c_html.encode('unicode_escape'))
                for i in c.xpath('//div[@class="WB_text"]'):
                    user, comment = i.xpath('string(.)').encode('utf-8').decode('unicode_escape').strip().split('：', maxsplit=1)
                    # print(f'{user}:{comment}')
                    self.db.add(user, comment)
                    if user == self.user:
                        print(f'{user}:{comment}')

    def run(self):
        self._base()
        self.getcomments()
        self.db.close()

if __name__ == '__main__':
    init_url = input('请输入微博链接:')
    username = input('请输入用户名:')
    wc = WeiboComment(init_url, username)
    wc.run()
