# -*- coding: utf-8 -*-
# Author: ElvisCT
# Function: 爬取百度首页
# Time: 2019年6月8日

import requests
import re
from lxml.html import etree
import os
import json
from multiprocessing import Process
import time
a = time.time()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}
url = "http://www.site.baidu.com/"


def get_page(url):
    """
    拿到 http://www.site.baidu.com/ 的部分代码
    :param url: url 链接
    :return: 网页代码
    """
    try:
        response = requests.get(url=url, headers=headers, timeout=15)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        else:
            return None
    except requests.RequestException as e:
        print('exception:', e.args)
        return None


def parse_page(html):
    """
    html 解析
    :param html: html代码
    :return: 解析出来的 titie 和 url
    """
    try:
        html = re.sub("\u3000", "", html)  # 去掉空格
        html = etree.HTML(html)
        lis = html.xpath("/html/body/div[2]/div[1]/div[2]/div[1]/ul/li")
        for li in lis:
            title = li.xpath(".//a/text()")
            title_c = "·".join(title)
            for i, item in enumerate(title):
                title[i] = title_c + " - " + item
            url = li.xpath(".//a/@href")
            
            info = dict(zip(title, url))
            for key, value in info.items():
                yield {
                    key: value,
                }
    except Exception:
        return None


def save_url(info):
    """
    文件保存
    :param info: 要保存的信息
    :return: None
    """
    if info:
        with open("save_url.json", "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)


def get_web_page(title_url, save_path="save_page"):
    """
    保存网页
    :param title_url: 网页的 title 和 url
    :param save_path: 保存路径
    :return: None
    """
    title_url = list(title_url.items())
    title = title_url[0][0]
    url = title_url[-1][-1]
    html = get_page(url)
    if html:
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        with open("{}/{}.html".format(save_path, title), "wb") as f:
            f.write(html.encode())
            f.flush()
        print("over", url)
        

def main():
    """
    运行主函数，程序调度
    :return: None
    """
    html = get_page(url=url)
    title_url = parse_page(html=html)
    title_url = list(title_url)
    save_url(title_url)
    ths = []  # 多线程爬取
    for item in title_url:
        # get_web_page(item)
        th = Process(target=get_web_page, args=[item])
        ths.append(th)
        print(item)
    for th in ths:
        th.start()
    for th in ths:
        th.join()


if __name__ == '__main__':
    main()
    print(time.time()-a)