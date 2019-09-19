# -*- coding: utf-8 -*-
# Function : 
# Author : Elvis CT
# Time : 2019年月日

import os
from time import time

import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread


# 获取所有表情包的网页链接
class DownloadBiaoqingbao(Thread):
    def __init__(self, queue, path):
        Thread.__init__(self)
        self.queue = queue
        self.path = path
        # if not os.path.exists(path):
        #     os.makedirs(path)

    def run(self):
        """
        多线程运行
        :return: None
        """
        while True:
            url = self.queue.get()
            try:
                # print(url, self.path)
                download_biaoqingbaos(url, self.path)
            finally:
                self.queue.task_done()


def download_biaoqingbaos(url, path):
    """
    表情包下载
    :param url: 表情包所在的网页链接
    :param path: 存储地址
    :return: None
    """
    response = requests.get(url)
    # 解析表情包的详情链接 <img.*?> 得到 img_list 列表
    soup = BeautifulSoup(response.content, 'lxml')
    img_list = soup.find_all('img', class_='ui image lazy')

    for img in img_list:
        image = img.get('data-original')  # 解析出图片的绝对url
        title = img.get('title')  # 解析出图片的名字
        print('下载图片： ', title)

        try:
            with open("%s/%s.jpg" % (path, title), 'wb') as f:
                img = requests.get(image).content
                f.write(img)
        except OSError:
            print('length  failed')


if __name__ == '__main__':

    start = time()

    # 构建所有的链接
    MIN_PAGE = 1
    MAX_PAGE = 200
    url = 'https://fabiaoqing.com/biaoqing/lists/page/{page}.html'
    urls = [url.format(page=page) for page in range(MIN_PAGE, MAX_PAGE+1)]

    queue = Queue()  # 创建队列
    path = '表情包'
    if not os.path.exists(path=path):
        os.makedirs(path)

    # 创建线程
    for x in range(10):
        worker = DownloadBiaoqingbao(queue, path)
        worker.daemon = True  # 守护进程
        worker.start()

    # 加入队列
    for url in urls:
        queue.put(url)

    queue.join()

    print('下载完毕耗时：  ', time()-start)

