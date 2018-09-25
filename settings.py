import os
import sys

HOME = os.path.expanduser('~')
DATA_DIR = os.path.join(HOME, 'weibo')
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

# For mysql
HOST = '127.0.0.1'
USER = 'root'
PASSWORD = '123456'
DB = 'weibo'

# For weibo
WEIBO_URL = 'https://weibo.com/1265020392/GAJt8tfqu?filter=hot&root_comment_id=0&type=comment'
USERNAME = 'Archean_w'
HEADERS = {
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/57.0.2987.133 Safari/537.36",
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
PROXIES = [
            {'https': 'http://191.101.175.185:8118', 'http': 'http://191,101,175,185:8118'},
            None
        ]
TIMEOUT = 5
COOKIES = os.path.join(DATA_DIR, 'weibo.cks')

# For log
LOG_FILE = os.path.join(DATA_DIR, 'weibo.log')
LOG_LEVEL = 'info'
