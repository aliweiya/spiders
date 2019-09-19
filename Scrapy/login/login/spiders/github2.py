# -*- coding: utf-8 -*-
import scrapy
import re

class Github2Spider(scrapy.Spider):
    name = 'github2'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,  # 自动的从 response 中寻找 表单
            formdata={"login":"ares15138122561", "password":"151381chuang5274"},
            callback = self.after_login
        )

    def after_login(self, response):
        print(re.findall("ares15138122561|Ares15138122561", response.body.decode()))
