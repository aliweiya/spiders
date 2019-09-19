# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
import os
import requests

os.chdir('E:\Python\Projects\Scrapy\MM131')
list_img = set(os.listdir('./save_img'))


class Mm131SpiderSpider(scrapy.Spider):
    name = 'mm131_spider'
    allowed_domains = ['m.mm131.net']
    start_urls = ['https://m.mm131.net/more.php?page=1']
    page = 2

    def parse(self, response):
        articles = response.xpath('//article')
        for article in articles:
            article_url = article.xpath('.//div/a/@href').get()
            yield scrapy.Request(url=article_url, callback=self.article_parse)

        next_page_url = 'https://m.mm131.net/more.php?page={0}'.format(self.page)
        if self.page < 506:
            self.page += 1
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def article_parse(self, response):
        src = response.xpath('//*[@id="content"]/article/div/a/img/@src').get()
        alt = response.xpath('//*[@id="content"]/article/div/a/img/@alt').get()
        self.save_img(src=src, alt=alt, referer=response.url)
        # yield scrapy.Request(url=src, callback=self.save_img, headers=headers, meta=(dict(src=src, alt=alt)))
        # print(src, alt)

        next_base_url = response.xpath('//*[@id="content"]/article/div/a[last()]/@href').get()
        if next_base_url:
            next_url = urljoin(response.url, next_base_url)
            yield scrapy.Request(url=next_url, callback=self.article_parse)

    def save_img(self, src, alt, referer):
        if alt:
            fileName = alt + '.jpg'
            if fileName not in list_img:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                    'Referer': referer,
                }
                if not os.path.exists('save_img'):
                    os.mkdir('save_img')
                file = './save_img/' + fileName
                response = requests.get(url=src, headers=headers, timeout=5)
                with open(file, 'wb') as f:
                    print(src, alt)
                    f.write(response.content)


