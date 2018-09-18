import sys

# For mysql
HOST = '127.0.0.1'
USER = 'root'
PASSWORD = '123456'
DB = 'weibo'

# For weibo
WEIBO_URL = 'https://weibo.com/1265020392/Gvpm1EU7O?filter=hot&root_comment_id=0&type=comment'
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

# For log
if sys.platform == 'win32':
    LOG_FILE = 'D:/Users/T00006732/log/weibo.log'
else:
    LOG_FILE = '/Users/archean/log/weibo.log'

LOG_LEVEL = 'info'
