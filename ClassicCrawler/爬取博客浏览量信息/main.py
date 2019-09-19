# -*- encoding: utf-8 -*-
"""
Created On 2019-08-30 10:30

Module Environment: python 3.6.0

@Module Function: 获取CSDN博客博主的博客信息

@Author: 漫天丶飞雪
"""

import requests
from lxml.html import etree
import re
from datetime import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',}


def get_page(url):
    """
    请求网页内容
    :param url: 要请求的网页链接
    :return: 请求返回的内容
    """
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
    except requests.RequestException as e:
        print('ERROR :', e.args)
        return None


def os_time():
    print('-' * 30)
    now = datetime.now()
    print("时间 : {}/{}/{} {}:{}:{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second))


def main(url):
    """
    调度函数
    :param url: 要检测的url链接
    :return: None
    """
    text = get_page(url)

    html = etree.HTML(text)
    visit, integral = html.xpath('//div[@class="grade-box clearfix"]/dl/dd/@title')
    ranking = html.xpath('//div[@class="grade-box clearfix"]/dl/@title')[0]
    riginal, fans, like, comment = html.xpath('//div[@class="data-info d-flex item-tiling"]/dl/@title')

    author = re.findall('var nickName = "(.*?)";', text, re.S)[0]

    os_time()
    print('-' * 30)
    print('作者 :', author)
    try:
        articleTitles = html.xpath('//p[@class="description "]/text()')[0]
        print('签名 :', articleTitles)
        # '<p class="description ">Python | 数据挖掘 | 数据分析 | 高并发数据采集</p>'
    except Exception:
        articleTitles = re.findall('var articleTitles = "(.*?)";', text, re.S)[0]
        print('-' * 30)
        print('标题 :', articleTitles)
    print('-' * 30)
    print('积分 :', integral)
    print('排名 :', ranking)
    print('访问 :', visit)
    print('-' * 30)
    print('原创 :', riginal)
    print('粉丝 :', fans)
    print('喜欢 :', like)
    print('评论 :', comment)
    print('-' * 30)


if __name__ == '__main__':
    url = 'https://blog.csdn.net/qq_39377418'
    main(url)





