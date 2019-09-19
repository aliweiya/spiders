# !/usr/bin/env python3  # linux下生效
# -*- ecoding: utf-8 -*-
# @TestEnv: python 3.6.0
# @ModuleName: test
# @Function: 
# @Author: 漫天丶飞雪
# @Date: 2019/7/13 16:00

import requests
from lxml.html import etree
import threading
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Referer': 'https://www.7160.com/fengjing/',
}
def get_page(url):
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response
        else:
            return False
    except requests.RequestException as e:
        print(e.args)
        return False

def parse_page(response):
    response = response
    html = etree.HTML(response.text)
    lis = html.xpath('//li')
    for li in lis:
        try:
            title = li.xpath('.//img/@alt')[0]
            src = li.xpath('.//img/@src')[0]
            yield title,src
        except Exception:
            pass

def save_src(title, src):
    file = 'saveSrc'
    if not os.path.exists(file):
        os.mkdir(file)
    savePath = "{0}/{1}.jpg".format(file, title)
    try:
        response = get_page(url=src)
        with open(savePath, 'wb') as f:
            f.write(response.content)
            print('saving ...', title, src)
    except Exception as e:
        print('save error...', e.args)


def get_one_page(base_url, offset):
    url = base_url.format(offset=offset)
    response = get_page(url)
    if response:
        items = parse_page(response)
        for title, src in items:
            print(title, src)
            save_src(title, src)
def run():
    MIN_PAGE = 1
    MAX_PAGE = 19
    base_url = "https://www.7160.com/fengjing/list_14_{offset}.html"
    ths = []
    for offset in range(MIN_PAGE, MAX_PAGE+1):
        ths.append(threading.Thread(target=get_one_page, args=[base_url, offset]))

    for th in ths:
        th.start()
    for th in ths:
        th.join()



if __name__ == '__main__':
    run()



