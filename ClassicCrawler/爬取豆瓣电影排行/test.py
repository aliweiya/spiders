# -*- coding: utf-8 -*-
# Author: ElvisCT
# Function: 爬取豆瓣电影排行
# Time: 2019年6月7日

import requests
from urllib.request import urlretrieve
import os
import re
from lxml.html import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}
base_url = "https://movie.douban.com/top250?start={offset}&filter="


# 爬取豆瓣电影排行
class DouBanRank(object):
    def __init__(self, offset, f):
        self.offset = offset  # 页码
        self.url = base_url.format(offset=self.offset)  # 爬去的url
        self.headers = headers
        self.f = f  # 数据保存
        # self.db = db
        # self.cursor = cursor
    
    def get_page(self):
        """
        拿到每页的豆瓣源码
        :return: 每页的豆瓣源码
        """
        try:
            response = requests.request(method="get", url=self.url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                response.encoding = response.apparent_encoding
                return response.text
            else:
                print("Request Error", response.status_code)
                return None
        except requests.RequestException as e:
            print("Request Exception", e.args)
            return None
    
    def save_info(self, info):
        """
        保存提取后的影视信息
        :param info: 提取后的影视信息
        :return: None
        """
        self.f.write(str(info))
        self.f.write("\n")
        self.f.flush()
    
    def parse_page(self):
        """
        影视信息解析
        :return: None
        """
        html = self.get_page() 
        if html:
            for i in range(25):
                html = re.sub("&nbsp;", "", html, re.S)
            html = etree.HTML(html)
            lis = html.xpath('//div[@id="content"]/div/div[@class="article"]/ol/li')
            for li in lis:
                info = dict()
                info["ranking"] = li.xpath('.//em/text()')[0]  # 排名
                info["title"] = li.xpath('.//span[@class="title"]/text()')[0]  # 电影名字
                info["artist"] = li.xpath('.//p[@class=""]/text()')[0].strip()  # 艺人
                info["type"] = li.xpath('.//p[@class=""]/text()')[1].strip()  # 影视类型
                info["score"] = li.xpath('.//span[@class="rating_num"]/text()')[0]  # 影视评分
                info["comment_count"] = li.xpath('.//div[@class="star"]/span[4]/text()')[0]  # 评论人数
                info["outline"] = li.xpath('.//span[@class="inq"]/text()')[0]  # 概要
                
                self.save_info(list(info.items()))
                print(info)
    
    def run(self):
        """
        运行程序
        :return: None
        """
        self.parse_page()


def main():
    """
    主函数
    :return: None
    """
    MAX_PAGE = 10
    f = open("DouBanRank.txt", "w", encoding="utf-8")
   
    for offset in range(MAX_PAGE):
        douban = DouBanRank(offset*25, f)
        douban.run()

    f.close()


if __name__ == '__main__':
    main()

