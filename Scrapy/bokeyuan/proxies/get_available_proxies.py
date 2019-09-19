"""
运行环境 : python3.6.0
模块功能 : 从代理网站获取公开IP代理，并检测公开IP代理的可用性，并将可用IP代理保存到 ./proxies.txt
"""

import requests
from pyquery import PyQuery as pq
import threading
import re


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    """
    从网上获取代理并以列表的形式返回
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0',
        }

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            # print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=10):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        try:
            urls = [start_url.format(page) for page in range(1, page_count + 1)]
            # print('Crawling', urls)
            for url in urls:
                # print('Crawling', urls)
                html = requests.get(url, headers=self.headers).text
                if html:
                    doc = pq(html)
                    # print(doc)
                    trs = doc('.containerbox table tr:gt(0)')
                    for tr in trs.items():
                        ip = tr.find('td:nth-child(1)').text()
                        port = tr.find('td:nth-child(2)').text()
                        yield ':'.join([ip, port])
        except requests.ConnectionError as e:
            print('Error ', e.args)

    def crawl_goubanjia(self):
        """
        获取 Goubanjia
        :return: 代理
        """
        start_url = 'http://www.goubanjia.com/'
        # print('Crawling', start_url)
        try:
            html = requests.get(start_url, headers=self.headers).content.decode('utf-8')
            if html:
                doc = pq(html)
                tds = doc('td.ip')
                for td in tds.items():
                    td.find('p').remove()
                    yield td.text().replace(' ', '').replace('\n', '').replace('\n', '')
        except requests.ConnectionError as e:
            print('Error ', e.args)

    def xici(self):
        url = 'https://www.xicidaili.com/'
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                trs = re.findall('<tr.*?>.*?</tr>', response.text, re.S)
                for tr in trs:
                    proxy_port = re.findall('<td.*?>(\d+.\d+.\d+.\d+)</td>.*?<td.*?>(\d+)</td>', tr, re.S)
                    if proxy_port:
                        proxies = ':'.join(list(proxy_port[0]))
                        yield proxies
                    else:
                        print('lalala')
            print(response.status_code)
        except requests.RequestException as e:
            print(e.args)


class IpAvailableRedirect(threading.Thread):  # 继承多线程
    def __init__(self, proxy, redirect_url='http://httpbin.org/get'):
        threading.Thread.__init__(self)
        self.proxy = proxy
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        }

        self.redirect_url = redirect_url
        self.proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }

    def __del__(self):
        pass

    def run(self):
        try:
            response = requests.get(self.redirect_url, headers=self.headers, proxies=self.proxies, timeout=5)
            if response.status_code == 200:
                print(self.redirect_url, '\t\t\t', 'request:', self.proxy, '\t', 'code: 200')
                with open('proxies.txt', 'a', encoding='utf-8') as f:  # 存储有效代理，初始化
                    f.write('"%s",\n' % self.proxy)
                return True
            else:
                print('request:', self.proxy, 'code:', response.status_code)
                return False
        except Exception as e:
            # print(e.args)
            return False


if __name__ == '__main__':
    crawl = Crawler()
    proxies = list(crawl.crawl_daili66())  # xici 或者 daili666 网站获取

    for item in crawl.crawl_daili66():  # 打印输出爬取的代理
        print(item)
        pass

    # 高并发批量检测代理的可用性，并存储可用代理至 proxies.txt
    with open('proxies.txt', 'w', encoding='utf-8') as f:  # 存储有效代理，初始化
        f.write('')
    redirect_url = 'https://www.cnblogs.com'
    ths = []
    for proxy in proxies:
        # proxy = '27.159.165.181:9999'
        agent_redirect = IpAvailableRedirect(proxy=proxy, redirect_url=redirect_url).run
        th = threading.Thread(target=agent_redirect, args=[])
        ths.append(th)
    for th in ths:
        th.start()
    for th in ths:
        th.join()
