# -*- encoding: utf-8 -*-
# Author: ElvisCT
# Function: 爬取itcast
# Time: 2019年6月2日

from scrapy.cmdline import execute

# execute(argv=['scrapy', 'crawl', 'quotes'])
execute('scrapy crawl itcast'.split())
