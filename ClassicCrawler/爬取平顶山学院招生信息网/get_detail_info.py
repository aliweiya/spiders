import requests
from settings import *
import re
from random import choice
from threading import Thread

count = 0


def get_url():
    with open('enrollment_info.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    urls = []
    for line in lines:
        urls.append(line.split('\t')[1])
    return urls


def get_available_proxies():
    with open('available_proxies.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if line:
            proxies = {
                'http': 'http://' + line.strip(),
                'https': 'https://' + line.strip(),
            }
            print(proxies)
            try:
                # print('retry proxies')
                text_url = 'http://zsxx.pdsu.edu.cn/info/1004/1121.htm'
                response = requests.get(text_url, headers=headers, proxies=proxies, timeout=5)
                if response.status_code == 200:
                    return proxies
                else:
                    continue
            except:
                continue


class DetailInfo(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.headers = headers
        self.url = url

    def get_page(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                global count
                count += 1
                print(count, self.url, response.status_code)
                response.encoding = response.apparent_encoding
                return response
            else:
                print('Retry', self.url, response.status_code)
                self.run()
        except requests.RequestException:
            print('Retry', count+1, self.url)
            self.run()

    def parse_page(self):
        response = self.get_page()
        st = re.findall('<tbody.*?>.*?</tbody>', response.text, re.S)[0]
        # print(st)
        trs = re.findall('<tr.*?>.*?</tr>', st, re.S)
        for tr in trs:
            if re.findall('<span.*?>(.*?)</span>', tr, re.S):
                result = re.findall('<span.*?>(.*?)</span>', tr, re.S)
            elif re.findall('<td.*?>(.*?)</td>', tr, re.S):
                result = re.findall('<td.*?>(.*?)</td>', tr, re.S)
            if len(result) == 5:  # 判断，如果长度为5，说明这个专业分为文理科
                result.insert(0, major)
            elif len(result) == 6:  # 判断，如果长度为6，可能下一项长度为5或6，就让下一项插入这个的第一项
                major = result[0]
            print(result)

    def run(self):
        self.parse_page()


def main():
    # proxies = get_available_proxies()
    for url in get_url():
        DetailInfo(url.strip()).run()
    # ths = []
    # for url in get_url():
    #     detail_info = DetailInfo(url.strip())
    #     ths.append(detail_info.run())
    # for th in ths:
    #     th.start()
    # for th in ths:
    #     th.join()


if __name__ == '__main__':
    main()
