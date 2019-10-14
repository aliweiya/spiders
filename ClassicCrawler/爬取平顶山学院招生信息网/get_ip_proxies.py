import json
import requests
import re
from threading import Thread

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
}

class Crawler(object):
    """
    从网上获取代理并以列表的形式返回
    """
    def __init__(self):
        self.headers = headers

    def crawl_goubanjia(self):
        """
        获取 Goubanjia
        :return: 代理
        """
        base_url = 'http://www.superfastip.com/welcome/freeip/{}'
        for offset in range(1, 11):
            try:
                response = requests.get(base_url.format(offset), headers=self.headers)
                if response.status_code == 200:
                    tbody = re.findall("""<tbody.*?>.*?</tbody>""", response.text, re.S)[1]
                    trs = re.findall("""<tr.*?>.*?</tr>""", tbody, re.S)
                    for tr in trs:
                        tr = re.findall("""<td.*?>(.*?)</td>""", tr, re.S)
                        proxy = tr[0] + ":" + tr[1]
                        yield proxy
            except requests.RequestException as e:
                print('Error ', base_url, e.args)
                return None


class IpProxiesAvailable(Thread):
    def __init__(self, proxies, file_open):
        Thread.__init__(self)  # 多线程初始化
        self.proxies = proxies
        self.f = file_open
        self.headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
        }
        # self.redirect_url = 'http://httpbin.org/get'
        self.redirect_url = 'https://www.baidu.com'
        self.proxy = {
            'http': 'http://' + self.proxies,
            'https': 'https://' + self.proxies,
        }

    def run(self):
        """
        运行，检测代理可用性
        :return: True or False
        """
        try:
            response = requests.get(self.redirect_url, headers=self.headers, proxies=self.proxy, timeout=5)
            if response.status_code == 200:
                print('request:', self.proxies, 'code: 200')
                self.f.write(self.proxies)
                self.f.write('\n')
                self.f.flush()
            else:
                print('request:', self.proxies, 'code:', response.status_code)
        except Exception:
            print('request:', self.proxies, 'Exception')


def availavle_proxies(ip_proxioes):
    """
    检测代理的可用性，并将可用代理写入本地 available_proxies.txt
    :param ip_proxioes: 要检测的代理列表
    :return: None
    """
    f = open('available_proxies.txt', 'w', encoding='utf-8')
    ths = []
    for item in ip_proxioes:
        agent_redirect = IpProxiesAvailable(item, f).run()
        ths.append(agent_redirect)
    for th in ths:
        th.start()
    for th in ths:
        th.join()
    f.close()


def get_ip_proxies():
    """
    获取网络免费代理
    :return: None
    """
    crawl = Crawler()
    ip_proxioes = crawl.crawl_goubanjia()  # 获取公开免费代理
    ip_proxioes = list(ip_proxioes)
    print(ip_proxioes)  # 正常

    availavle_proxies(ip_proxioes)  # 检测获取到的代理的可用性


if __name__ == '__main__':
    result = get_ip_proxies()
    print(result)

