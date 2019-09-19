# -*- encoding: utf-8 -*-
"""
Created On 2019-05-05 12:22

Module Environment: python 3.6.0

@Module Function: 获取博主的多个博客链接

@Author: 漫天丶飞雪
"""

import requests


def get_max_page():
    url = 'https://rabc1.iteye.com/source/h751.js?avneunkw=b'
    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
    }
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            import re
            max_type = re.findall('mixType:(.*?),', response.text)
            return int(max_type[0].strip())
        else:
            return None
    except Exception:
        return None


class GetUrls(object):
    def __init__(self, max_page):
        self.headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
        }
        self.max_page = max_page
        # url = 'https://blog.csdn.net/qq_39377418/article/details/89816398'
        self.url = 'https://blog.csdn.net/qq_39377418//article/list/{num}?'

    def get_page(self, num):
        url = self.url.format(num=str(num))
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 200:
                response.encoding = response.apparent_encoding
                return response.text
        except Exception:
            print('Error')
            return None

    def parse_html(self, num):
        html = self.get_page(num)
        if html:
            import re
            pattern = """<a href="(https://blog.csdn.net/qq_39377418/article/details/.*?)".*?>"""
            urls = re.findall(pattern, html, re.S)
            return urls
        else:
            return None

    def run(self):
        all_urls = []
        for num in range(1, self.max_page+1):
            urls = self.parse_html(num)
            if urls:
                all_urls.extend(urls)
                # print('page',num, '\t\t', 'urls', set(urls))
            else:
                pass
        all_urls = set(all_urls)
        # print(all_urls)
        return all_urls


def run():
    """
    运行程序
    :return:
    """
    max_type = get_max_page()  # 获取博主博客的最大页数
    max_type = 6
    agent = GetUrls(max_type)  # 获取所有页的所有url
    result = agent.run()
    return result


if __name__ == '__main__':
    res = run()
    with open('urls.txt', 'w') as f:
        for i, item in enumerate(res):
            f.write(item)
            f.write('\n')
            print(i+1, item)
