# -*- coding: utf-8 -*-
import scrapy
import re

class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/971252285/profile']

    def start_requests(self):
        cookies = 'anonymid=jx5vpf7mfs95qz; depovince=ZGQT; _r01_=1; JSESSIONID=abc_B29QYO7-ud0Wzu5Tw; jebe_key=da51da52-0b3b-4c81-8325-1ec5279c80bd%7C300914a2b4851a42efe43818873961c0%7C1561108560820%7C1%7C1561108558249; XNESSESSIONID=8004b80b3d70; ick=537179ff-5bc4-4db7-bb66-d4526b5303f9; jebecookies=7eae80c5-1cb7-44ba-bac4-43dab21035f8|||||; ick_login=acbc833a-d444-4b58-88b0-c3bea41b1300; _de=7C03D95DD89664170ADE65415FC01940; p=b2289d21c215cf7078196932d126b24c5; first_login_flag=1; ln_uact=15138122561; ln_hurl=http://hdn.xnimg.cn/photos/hdn421/20190621/1715/h_main_lxIi_ce0d000acdb61986.jpg; t=6e30e25874f247cdf3e2e505b4cf4ff45; societyguester=6e30e25874f247cdf3e2e505b4cf4ff45; id=971252285; xnsid=86a529a4; ver=7.0; loginfrom=null; wp_fold=0'
        cookies = {i.split('=')[0].strip(): i.split('=')[1].strip() for i in cookies.split(';')}
        # headers = {'cookie': cookies}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            # cookies= cookies,
            # headers=headers,
        )

    def parse(self, response):
        res = re.findall('ElvisCT', response.body.decode())
        print(res)
        yield scrapy.Request(
            'http://www.renren.com/971252285/profile?v=info_timeline',
            callback=self.parse_detail,
        )

    def parse_detail(self, response):
        res = re.findall('ElvisCT', response.body.decode())
        print(res)
