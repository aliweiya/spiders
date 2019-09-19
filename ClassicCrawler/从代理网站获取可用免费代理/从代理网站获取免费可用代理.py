# -*- encoding: utf-8 -*-
"""
Created On 2019-05-04 ‏‎21:27

Module Environment: python 3.6.0

@Module Function:

@Author: 漫天丶飞雪
"""

import requests
from random import choice
import get_csdn_url
from concurrent.futures.thread import ThreadPoolExecutor
from randomUA import user_agents_all
import threading
import os
import datetime
import sys

sys.stdout.flush()
os.chdir('E:\Python\Projects\不是闹着玩儿嘞\exercise\从代理网站获取可用免费代理')  # 切换目录


class GetIpAgent(object):  # 从ip代理网站获取免费 ip 代理
    def __init__(self):
        self.headers = {
            'User-Agent': choice(user_agents_all),
        }
        self.ip_agent_url = 'http://gec.ip3366.net/api/?key=20181214170452135&getnum=100&anonymoustype=4&area=1&order=2&formats=2&proxytype=0'
        # url = 'https://blog.csdn.net/qq_39377418/article/details/89816398'

    def get_page(self):
        """
        访问 ip 代理网站
        :return: 代理网站返回的 json 数据
        """
        try:
            response = requests.get(url=self.ip_agent_url, headers=self.headers)
            return response.json()
        except Exception:
            return None

    def get_ip_all_agent(self):
        """
        从 json 数据中提取 ip 代理
        :return:  ip 代理
        """
        ip_all_data = self.get_page()
        ips = []
        for item in ip_all_data:
            ip = item.get('Ip') + ':' + str(item.get('Port'))
            ips.append(ip)
        return ips

    def run(self):
        """
        将提取到的 ip 代理保存到本地 (proxies_all.txt)
        :return:
        """
        proxies = self.get_ip_all_agent()
        with open('proxies_all.txt', 'w', encoding='utf-8') as f:
            for proxie in proxies:
                f.write(str(proxie))
                f.write('\n')
        return proxies


class IpAvailableRedirect(threading.Thread):  # 继承多线程
    def __init__(self, proxy, rand_url):
        threading.Thread.__init__(self)
        self.proxy = proxy
        self.headers = {
            'User-Agent': choice(user_agents_all),
            'Referer': 'https://blog.csdn.net/qq_39377418',
            'Host': 'blog.csdn.net',
            'Upgrade-Insecure-Requests': '1',
        }

        # self.redirect_url = 'https://blog.csdn.net/qq_39377418/article/details/97262955'
        self.redirect_url = rand_url
        self.proxies = {
            'http': 'http://' + self.proxy,
            'https': 'https://' + self.proxy,
        }

    def __del__(self):
        pass

    def run(self):
        try:
            response = requests.get(self.redirect_url, headers=self.headers, proxies=self.proxies, timeout=5)
            if response.status_code == 200:
                print(self.redirect_url, '\t\t\t', 'request:', self.proxy, '\t',  'code: 200')
                return True
            else:
                print('request:', self.proxy, 'code:', response.status_code)
                return False
        except Exception as e:
            return False


def get_time():
    with open('./time.txt', 'a+', encoding='utf-8') as f:
        time = str(datetime.datetime.now()).split('.')[0]
        f.write(time + '\n')


def main():
    """ 保存最新运行时间 """
    get_time()

    """ 获取要爬取的 urls """
    # urls = tuple(get_csdn_url.run())
    with open('./urls.txt', 'r', encoding='utf-8') as f:
        urls = f.readlines()
        urls = [url.strip() for url in urls]

    """ 获取 proxies """
    # with open('./proxies_all.txt', 'r', encoding='utf-8') as f:
    #     lines = f.readlines()
    # proxies = [line.strip() for line in lines if line]
    agent_get = GetIpAgent()
    proxies = agent_get.run()

    ths = []
    for proxy in proxies:
        agent_redirect = IpAvailableRedirect(proxy=proxy, rand_url=choice(urls)).run
        th = threading.Thread(target=agent_redirect, args=[])
        ths.append(th)
    for th in ths:
        th.start()
    for th in ths:
        th.join()


if __name__ == '__main__':
    main()

