#!/usr/bin/env python3

import re
import grequests
import requests
from lxml import etree

class WeiboComment(object):
    def __init__(self, weibo_url, cookies, username):
        self.urls = []
        self.user = username
        self.weibo_url = weibo_url
        self.cookies = dict(i.split('=') for i in cookies.split(';'))
        self.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'accept-encoding':'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }

    def getbase(self):
        a = requests.get(self.weibo_url, headers=self.headers, cookies=self.cookies)
        totalcomment = int(re.findall(r'<em>(\d+)<\\/em>', a.text)[1])
        if totalcomment%20 ==0:
            totalpage = totalcomment//20
        else:
            totalpage = totalcomment//20 + 1
        weibo_id = re.findall(r'\\"id=(\d+)&filter', a.text)[0]
        print('总共%s页,%s评论' % (totalpage, totalcomment))
        for page in range(1, totalpage+1):
            base_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=%s&filter=all&page=' % (weibo_id)
            c_url = base_url + str(page)
            self.urls.append(c_url)

    @staticmethod
    def exception_handler(request, exception):
        try:
            return requests.get(request.url, headers=self.headers, cookies=self.cookies)
        except:
            print(exception, request.url)

    def getcomments(self):
        tasks = (grequests.get(url, headers=self.headers, cookies=self.cookies) for url in self.urls)
        bs = grequests.map(tasks, size=10, exception_handler=self.exception_handler)
        for b in bs:
            if b:
                d = b.json()
                c_html = d['data']['html']
                c = etree.HTML(c_html)
                for i in c.xpath('//div[@class="WB_text"]'):
                    user, comment = i.xpath('string(.)').strip().split('：', maxsplit=1)
                    if user == self.user:
                        print('~~~~~~~~~~%s' % (comment))

    def run(self):
        self.getbase()
        self.getcomments()

if __name__=='__main__':
    weibo_url = input('请输入微博链接:')
    cookies = input('请输入cookies:')
    username = input('请输入用户名:')
    weibocomment = WeiboComment(weibo_url, cookies, username)
    weibocomment.run()
