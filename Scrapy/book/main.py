# -*- coding: utf-8 -*-
# Function : 
# Author : 
# Time : 2019年月日

from scrapy.cmdline import execute

with open('./suning.txt', 'w', encoding='utf-8') as f:
    f.write('')
execute("scrapy crawl suning".split(' '))


