import sys

# For mysql
HOST = '127.0.0.1'
USER = 'root'
PASSWORD = '123456'
DB = 'weibo'

# For weibo
WEIBO_URL = 'https://weibo.com/1265020392/Gwt7ZBtMz?filter=hot&root_comment_id=0&type=comment'
USERNAME = 'Archean_W'

# for log
if sys.platform == 'win32':
    LOG_FILE = 'D:/Users/T00006732/log/weibo.log'
else:
    LOG_FILE = '/Users/archean/log/weibo.log'

LOG_LEVEL = 'debug'
