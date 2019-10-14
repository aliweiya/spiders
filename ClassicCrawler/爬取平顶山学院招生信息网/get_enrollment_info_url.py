"""
功能：爬取平顶山学院招生官网 招生信息 的详细链接
注意：一般情况下第一次爬第一张的时候会不给你真是数据，重试就可以了，程序已经重试过了
"""
import requests
import re
from settings import *


class GetPdsuEnrollmentInformationUrl(object):
    def __init__(self):
        self.base_title_url = 'http://zsxx.pdsu.edu.cn/zsxx/'
        self.first_url = 'http://zsxx.pdsu.edu.cn/zsxx.htm'
        self.base_detail_url = 'http://zsxx.pdsu.edu.cn/'
        self.f = open('enrollment_info.txt', 'w', encoding='utf-8')
        self.enrollment_info = []
        self.headers = headers

    def get_page(self, url):
        """
        拿到招生信息网本页的招生信息的原网页代码
        :return: 招生信息网本页的招生信息的原网页代码
        """
        try:
            response = requests.get(url=url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                response.encoding = response.apparent_encoding
                # print(response.text)
                return response.text
            else:
                return None
        except requests.RequestException as e:
            print('Request Error:', e.args)
            return None

    def get_next_page_url(self, html):
        """
        解析下一页网页的path
        :param html: 本页的html源代码
        :return: 下一页网页的path
        """
        try:
            next_page_path = re.findall('''<span class="p_next p_fun"><a href="(.*?)">下页</a></span>''', html, re.S)[0]
            return next_page_path
        except:
            return None

    def parse_page(self, url='http://zsxx.pdsu.edu.cn/zsxx.htm'):
        """
        页面解析，解析内容为页面的 Enrollment Information Url
        :param url: 要解析的网页地址
        :return: None
        """
        html = self.get_page(url)
        if html:
            pattern = re.compile('<li id=".*?"><span>(.*?)</span> <a href="(.*?)".*?title=".*?">(.*?)</a></li>', re.S)
            name_url_date = re.findall(pattern, html)

            if name_url_date == []:  # 如果为解析到所需内容，则说明有反爬虫，就在来一遍（重新获取一下该网页）
                print('Retry...', url)
                self.parse_page()

            for item in name_url_date:  # 将该页的 enrollment_info 写入本地
                item = list(item)
                item[1] = self.base_detail_url + item[1].replace('../', '')

                item = "\t".join(item)
                self.f.write(item)
                self.f.write('\n')
                self.f.flush()

            self.enrollment_info.extend(name_url_date)  # 将enrollment_info存入列表

            next_page_path = self.get_next_page_url(html)  # 获取下一页地址
            if next_page_path:  # 如果存在下一页地址
                next_page_path = next_page_path.replace('zsxx/', '')
                self.parse_page(self.base_title_url + next_page_path)
            else:
                pass

    def run(self):
        """
        程序运行方法
        :return: 解析后的所有 Enrollment Information Url
        """
        self.parse_page()
        return self.enrollment_info


def enrollment_info_duplicate_removal():
    """
    解析后的所有 Enrollment Information Url 消重，保存入文件 enrollment_info_no_weight.txt
    :return: None
    """
    with open('enrollment_info.txt', 'r', encoding='utf-8') as f:
        info_url = f.readlines()
    with open('enrollment_info.txt', 'w', encoding='utf-8') as f:
        for item in set(info_url):
            f.write(item)
            f.flush()
            print('save url ing ...', item.strip())

def main():
    """
    主函数，这个程序的运行的入口
    :return:
    """
    GetPdsuEnrollmentInformationUrl().run()
    enrollment_info_duplicate_removal()


if __name__ == '__main__':
    main()
    print('Pdsu Enrollment Information Url Save Completed')



