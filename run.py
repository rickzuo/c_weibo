# !/usr/bin/env python3
# coding: utf-8

import logging
from weibo import WeiboComment
from settings import LOG_FILE, LOG_LEVEL

LEVEL = {'INFO': logging.INFO,
         'DEBUG': logging.DEBUG,
         'WARNING': logging.WARNING,
         'ERROR': logging.ERROR}
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILE, format=FORMAT, level=LEVEL[LOG_LEVEL])
logger = logging.getLogger('weibo')
logger.info('-' * 100)


def main():
    wb = WeiboComment()
    wb.run()


if __name__ == '__main__':
    main()
