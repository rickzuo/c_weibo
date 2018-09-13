# !/usr/bin/env python3
# coding: utf-8

import logging
from weibo import WeiboComment
from settings import LOG_FILE, LOG_LEVEL


def main():
    _level = {'INFO': logging.INFO,
              'DEBUG': logging.DEBUG,
              'WARNING': logging.WARNING,
              'ERROR': logging.ERROR}
    _format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=LOG_FILE, format=_format, level=_level[LOG_LEVEL.upper()])
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler()
    logger.info('-' * 100)
    wb = WeiboComment()
    wb.run()


if __name__ == '__main__':
    main()
