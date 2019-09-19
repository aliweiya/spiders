# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class XiciSpiderSpider(scrapy.Spider):
    name = 'xici_spider'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn/1']

    def parse(self, response):
        print(response)
        # soup = BeautifulSoup(response.text, 'lxml')
        # print(soup.prettify())
        trs = response.xpath('//table//tr')
        for tr in trs:
            ip = tr.xpath('.//td[2]/text()').get()
            port = tr.xpath('.//td[3]/text()').get()
            print(ip, port)

        next_url_param = response.xpath('//div[@class="pagination"]/a[last()]/@href').get()
        if next_url_param:
            next_url = urljoin(response.url, next_url_param)
            yield scrapy.Request(url=next_url, callback=self.parse)

