# -*- encoding: utf-8 -*-
"""
Created On 2019-07-26 13:01

Module Environment: python 3.6.0

@Module Function: 

@Author: 漫天丶飞雪
"""

import requests
from randomUA import user_agents_all
from random import choice


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


def save_proxies(proxies):
    try:
        if len(proxies) > 0:
            with open('./proxies_all.txt', 'w', encoding='utf-8') as f:
                for proxy in proxies:
                    f.write(str(proxy).strip())
                    f.write('\n')
                    f.flush()
    except Exception:
        pass


if __name__ == '__main__':
    agent_get = GetIpAgent()
    proxies = agent_get.run()
    save_proxies(proxies)


