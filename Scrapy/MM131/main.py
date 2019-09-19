# -*- encoding: utf-8 -*-
"""
Created On 2019-08-09 14:50

Module Environment: python 3.6.0

@Module Function: 

@Author: 漫天丶飞雪
"""

from scrapy.cmdline import execute
import os

if not os.path.exists('./save_img'):
    os.mkdir('./save_img')
os.chdir('E:\Python\Projects\Scrapy\MM131')
execute('scrapy crawl mm131_spider'.split())
# print()

