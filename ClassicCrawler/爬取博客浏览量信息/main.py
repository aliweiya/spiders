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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    # "Cookie": "uuid_tt_dd=10_19733214950-1572183051576-210324; dc_session_id=10_1572183051576.974951; UserName=qq_39377418; UserInfo=29dcc0169feb428c99b3c9558d378abd; UserToken=29dcc0169feb428c99b3c9558d378abd; UserNick=%E6%BC%AB%E5%A4%A9%E4%B8%B6%E9%A3%9E%E9%9B%AA; AU=EC1; UN=qq_39377418; BT=1572183073290; p_uid=U000000; acw_tc=2760827515722445325162278e527a3cc2011fabb18032d98d2f125ec71f1c; __gads=Test; smidV2=2019103120365449d8ef77895cedf1a4666f662fa7fc42008c633b58a4c1fe0; announcement=%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fblogdev.blog.csdn.net%252Farticle%252Fdetails%252F102605809%2522%252C%2522announcementCount%2522%253A0%252C%2522announcementExpire%2522%253A3600000%257D; acw_sc__v2=5dbd2164bfa09947dcb883d968ecad6eb8f6f31e; dc_tos=q0bwiz; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1572664371,1572665976,1572672670,1572672784; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1572675948; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_19733214950-1572183051576-210324!5744*1*qq_39377418!1788*1*PC_VC",
}


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
            # print(response.text)
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
    # 等级
    grade = html.xpath('//div[@class="grade-box clearfix"]/dl/dd/a/@title')[0].split(',')[0]
    # 积分
    integral = html.xpath('//div[@class="grade-box clearfix"]/dl/dd/@title')[0]
    # 周排名
    week_ranking = html.xpath('//div[@class="grade-box clearfix"]/dl/dd/a[@class="grade-box-rankA"]/text()')[0].strip()
    # 总排名
    ranking = html.xpath('//div[@class="grade-box clearfix"]/dl/@title')[0]
    original, fans, support, comment, visit = html.xpath('//div[@class="data-info d-flex item-tiling"]/dl/@title')
    # res = html.xpath('//div[@class="data-info d-flex item-tiling"]/dl/@title')
    # print(res)

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
    print('积分   :', integral)
    print('排名   :', ranking)
    print('周排名 :', week_ranking)
    print('等级   :', grade)
    # print('访问 :', visit)
    print('-' * 30)
    print('原创 :', original)
    print('粉丝 :', fans)
    print('获赞 :', support)
    print('评论 :', comment)
    print('访问 :', visit)
    print('-' * 30)


if __name__ == '__main__':
    url = 'https://blog.csdn.net/qq_39377418'
    main(url)
