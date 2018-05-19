#!/usr/bin/env python3

import random
import grequests
import requests
from lxml import etree

class WeiboComment(object):
    def __init__(self, weibo_id):
        self.urls = []
        #self.ips = requests.get('http://www.archean.wang/myapp/api').json()['proxies']
        self.weibo_id = weibo_id
        self.cookie = 'SINAGLOBAL=8396359549062.56.1521166888240; un=13006164624; UOR=,,login.sina.com.cn; wvr=6; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWdCfoP_u_3.TIQ-OCdIc_E5JpX5KMhUgL.FoeReKM7ehzNeK.2dJLoI7LWMJSQ9g8VPNMt; ALF=1558016340; SSOLoginState=1526480341; SCF=AuHVNxDDnFRIzMjUi0G3ZYFAX_o9t833I-6Dkeo6ZSw_4TO2tv3aPg2ppKeJuP1bn7aCjIR_HK0V7nnLWVmfTrI.; SUB=_2A253-E2FDeRhGeVG6lUR8CzLyjWIHXVUjDhNrDV8PUNbmtANLUzwkW9NT6lLoAuselI2QhPgw54jDt-oCnRybQwN; SUHB=0h1JdTP9Cy9AE6; YF-V5-G0=b8115b96b42d4782ab3a2201c5eba25d; _s_tentry=-; Apache=7108213375258.339.1526480351704; ULV=1526480351804:17:8:2:7108213375258.339.1526480351704:1526189395986; YF-Page-G0=091b90e49b7b3ab2860004fba404a078'
        self.cookies = dict(i.split('=') for i in self.cookie.split(';'))
        self.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'accept-encoding':'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        self.url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=%s&filter=all&page=' % (weibo_id)

    def getbase(self):
        a = requests.get(self.url+'1',headers=self.headers, cookies=self.cookies).json()
        totalpage =  a['data']['page']['totalpage']
        totalcomment = a['data']['count']
        print('总共%s页,%s评论' % (totalpage, totalcomment))
        for page in range(1, totalpage+1):
            c_url = self.url + str(page)
            self.urls.append(c_url)

    @staticmethod
    def exception_handler(request, exception):
        #print(request.kwargs['proxies']['https'])
        try:
            return requests.get(request.url, headers=self.headers, cookies=self.cookies)
        except:
            print(exception, request.url)

    def getcomments(self):
        #tasks = (grequests.get(url, headers=self.headers, cookies=self.cookies, timeout=5, proxies={'https':random.choice(self.ips)}) for url in self.urls)
        tasks = (grequests.get(url, headers=self.headers, cookies=self.cookies) for url in self.urls)
        bs = grequests.map(tasks, size=10, exception_handler=self.exception_handler)
        for b in bs:
            if b:
                d = b.json()
                c_html = d['data']['html']
                c = etree.HTML(c_html)
                for i in c.xpath('//div[@class="WB_text"]'):
                    user, comment = i.xpath('string(.)').strip().split('：', maxsplit=1)
                    if user == 'Mm-yyl':
                        print('~~~~~~~~~~%s' % (comment))

    def run(self):
        self.getbase()
        self.getcomments()

if __name__=='__main__':
    weibo_id = input('请输入微博ID:')
    weibocomment = WeiboComment(weibo_id)
    weibocomment.run()
