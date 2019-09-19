# -*- coding: utf-8 -*-
import scrapy
import re


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        authenticity_token = response.xpath('//input[@ name="authenticity_token"]/@value').extract_first()
        utf8 = response.xpath('//input[@name="utf8"]/@value').extract_first()
        commit = response.xpath('//input[@name="commit"]/@value').extract_first()
        post_data = dict(
            login = "ares15138122561",
            password = "151381chuang5274",
            authenticity_token = authenticity_token,
            utf8 = utf8,
            commit = commit,
        )
        yield  scrapy.FormRequest(
            'http://github.com/session',
            formdata=post_data,
            callback=self.after_login
        )
        print(authenticity_token)
    def after_login(self, response):
        with open('./github_session.html', 'w', encoding='utf-8') as f:
            f.write(response.body.decode('utf-8'))
        print(re.findall("ares15138122561|Ares15138122561", response.body.decode()))
        print(response.url)
