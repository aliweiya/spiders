# -*- coding: utf-8 -*-
import scrapy
import logging

logger = logging.getLogger(__name__)  # 实例化


class ItcastSpider(scrapy.Spider):
    name = 'itcast'  # 爬虫名
    allowed_domains = ['itcast.cn']  # 允许爬取的范围
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml#ac']  # 最开始请求的url地址

    def parse(self, response):
        # 这个方法名字，不能改，因为它是专门干这个事情的
        # 处理 start_url 地址对应的响应
        # response_text = response.xpath("//div[@class='tea_con']//h3/text()").extract()
        # print(response_text)

        response_text = response.xpath("//div[@class='tea_con']//li")
        for li in response_text:
            item = {}
            item['name'] = li.xpath(".//h3/text()").extract_first()
            item['title'] = li.xpath(".//h4/text()").extract_first()
            logger.warning(item)
            yield item

