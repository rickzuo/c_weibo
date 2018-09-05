# !/usr/bin/env python3
# coding：utf-8

import re
import grequests
import requests
from lxml import etree


class WeiboComment(object):
    def __init__(self, weibo_url,  username):
        self.urls = []
        self.user = username
        self.weibo_url = weibo_url
        # self.cookies = dict(i.split('=') for i in cookies.split(';'))
        self.headers = {
            'user-agent': 'spider',# 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }

    def _base(self):
        a = requests.get(self.weibo_url, headers=self.headers)
        comments = int(re.findall(r'<em>(\d+)<', a.text)[0])
        if comments % 20 == 0:
            pages = comments//20
        else:
            pages = comments//20 + 1
        weibo_id = re.findall(r'"id=(\d+)&filter', a.text)[0]
        print('总共%s页,%s评论' % (pages, comments))
        for page in range(1, pages+1):
            url = f'https://weibo.com/aj/v6/comment/big?ajwvr=6&id={weibo_id}&filter=all&page={page}'
            self.urls.append(url)

    @staticmethod
    def exception_handler(request, exception):
        try:
            return requests.get(request.url, headers=request.headers)
        except:
            print(exception, request.url)

    def getcomments(self):
        tasks = (grequests.get(url, headers=self.headers) for url in self.urls)
        bs = grequests.map(tasks, size=10, exception_handler=self.exception_handler)
        for b in bs:
            if b:
                d = b.json()
                c_html = d['data']['html']
                c = etree.HTML(c_html.encode('unicode_escape'))
                for i in c.xpath('//div[@class="WB_text"]'):
                    user, comment = i.xpath('string(.)').encode('utf-8').decode('unicode_escape').strip().split('：', maxsplit=1)
                    print(f'{user}:{comment}')
                    if user == self.user:
                        print(f'{user}:{comment}')

    def run(self):
        self._base()
        self.getcomments()

if __name__ == '__main__':
    init_url = input('请输入微博链接:')
    # cookies = input('请输入cookies:')
    username = input('请输入用户名:')
    weibocomment = WeiboComment(init_url, username)
    weibocomment.run()
