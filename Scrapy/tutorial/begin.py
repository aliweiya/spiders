from scrapy.cmdline import execute

# execute(argv=['scrapy', 'crawl', 'quotes'])
execute('scrapy crawl quotes'.split())
