# !/usr/bin/env python3
# coding: utf-8

import logging
from weibo import WeiboComment
from settings import LOG_FILE, LOG_LEVEL

_level = {'INFO': logging.INFO,
          'DEBUG': logging.DEBUG,
          'WARNING': logging.WARNING,
          'ERROR': logging.ERROR
          }
_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
handler.setLevel(_level[LOG_LEVEL.upper()])
formatter = logging.Formatter(_format)
handler.setFormatter(formatter)
logging.basicConfig(handlers=[handler], level=_level[LOG_LEVEL.upper()])
logger = logging.getLogger('root')


def main():

    logger.info('=' * 150)
    wb = WeiboComment()
    wb.run()


if __name__ == '__main__':
    main()
