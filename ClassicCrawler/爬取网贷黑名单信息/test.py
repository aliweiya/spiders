# -*- encoding: utf-8 -*-
"""
Created On 2019-07-18 10:23

Module Environment: python 3.6.0

@Module Function: 

@Author: 漫天丶飞雪
"""

import requests
import re
from lxml.html import etree
from urllib import parse
from concurrent.futures.thread import ThreadPoolExecutor
from bs4 import BeautifulSoup
import os
import json



class GetPage(object):
    def __init__(self):
        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, sdch',
            # 'Accept-Language': 'zh-CN,zh;q=0.8',
            # 'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
            'Referer': 'https://blog.csdn.net/xunalove/article/details/77938349?utm_source=app',  # 很重要
            # 'Cookie': 'ASPSESSIONIDSQRSCQR=JMDIDLGDLEJFHJDJGBIFNPNP; ASPSESSIONIDSQRRDQTR=OGEIELGDJHOILHIEJGLJNEEB; ASPSESSIONIDSQQQDRTQ=MLDIDLGDINCNOCPAKIKKMDLF; ASPSESSIONIDQSRTCRTR=DMDKDLGDKHGACNLAMCCCICFI; ASPSESSIONIDQQTTCQSQ=DPHNBBNDCJFHFEMLOICPNONB; ASPSESSIONIDSSRRCRSQ=MEDKCLGDEKPHFNNCDBHIHBIC; ASPSESSIONIDSQRQCRSQ=PFDICLGDLJBIMBDIFCGBGLII; ASPSESSIONIDQQTQCQTR=CJEEFLGDPABJNOEDLKJGKLFM; ASPSESSIONIDSSSSBQTQ=KJFOGLGDAJKPPOCGAGIOBDLI; __tins__4142117=%7B%22sid%22%3A%201563416933764%2C%20%22vd%22%3A%209%2C%20%22expires%22%3A%201563420493358%7D; __51cke__=; __51laig__=9',
            # 'Host': 'www.p2pjd.com',
            # 'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.session()

    def get_page(self, url):
        """
        获取请求的网页代码
        :param url: 网站链接
        :return: 请求的网页代码
        """
        try:
            response = self.session.request(method='get', url=url, headers=self.headers,  verify=False, timeout=5)
            if response.status_code == 200:
                response.encoding = response.apparent_encoding
                return response.text
            else:
                return None
        except requests.RequestException as e:
            print(url, e.args)
            return None


class GetDetailUrl(GetPage):
    def __init__(self):
        GetPage.__init__(self)
        self.start_url = "http://www.p2pjd.com/Article_Class_103.html"
        # self.start_url = 'http://www.p2pjd.com/Article_Class.asp?ID=103&page=3'
        self.details = []

    def parse_page(self, url=None):
        if not url:
            url = self.start_url
        """ 获取网页 """
        text = self.get_page(url)

        """ 获取网页的详情url信息 """
        # print(text)
        html = etree.HTML(text=text)
        lis = html.xpath('//div[@id="content"]/ul/li')
        for li in lis:
            detail_url = li.xpath('./a/@href')[0]
            detail_url = parse.urljoin(url, detail_url)
            self.details.append(detail_url)
            # print(detail_url)

        """ 获取下一页 """
        next_page_url = re.findall('<li><a href="(.*?)">(.*?)</a></li>', text, re.S)

        for item in next_page_url:
            if item[1].strip() == '下一页':
                next_page_url = parse.urljoin(self.start_url, item[0])
                # print(next_page_url)
                break
            else:
                next_page_url = None

        """ 如果存在下一页则继续请求下一页 """
        if next_page_url:
            self.parse_page(next_page_url)

        return self.details


class GetBlackList(GetPage):
    def __init__(self):
        super(GetBlackList, self).__init__()

    def parse_page(self, url):
        """ 获取网页源码 """
        text = self.get_page(url)
        """  很重要，因为发现其并不是完整的html结构，在这里做一下预处理 """
        text = re.findall('<html.*?>.*?</html>', text, re.S)[0]
        soup = BeautifulSoup(text, 'lxml')
        text = soup.prettify()

        html = etree.HTML(text=text)
        info = dict()
        info['时间-点击'] = html.xpath('//div[@id="web2l"]/h3/text()')[0].strip()
        legal_person = html.xpath('//div[@id="web2l"]//div[@id="content"]//text()')
        legal_person = [item.replace('\xa0', '').strip() for item in legal_person]
        legal_person = dict([item.split('：') for item in legal_person if len(item.split('：')) == 2])
        info.update(legal_person)
        print(url, info)
        # self.save_info(info)

    def save_info(self, saveInfo):
        file = 'saveInfo'
        if not os.path.exists(file):
            os.mkdir(file)
        filePath = os.path.join(os.getcwd(), file + r'\黑名单.json')
        with open(filePath, 'w+', encoding='utf-8') as f:
            json.dump(saveInfo, f, ensure_ascii=False, indent=4)

    def run(self, url):
        self.parse_page(url)


def main():
    # get_detail_url = GetDetailUrl()
    # detail_urls = get_detail_url.parse_page()
    #
    # for item in enumerate(detail_urls):
    #     print(item)

    detail_urls = ['http://www.p2pjd.com/News/34471.html', 'http://www.p2pjd.com/News/34470.html', 'http://www.p2pjd.com/News/33111.html', 'http://www.p2pjd.com/News/29194.html', 'http://www.p2pjd.com/News/29193.html', 'http://www.p2pjd.com/News/29192.html', 'http://www.p2pjd.com/News/29191.html', 'http://www.p2pjd.com/News/29190.html', 'http://www.p2pjd.com/News/29189.html', 'http://www.p2pjd.com/News/29188.html', 'http://www.p2pjd.com/News/29187.html', 'http://www.p2pjd.com/News/29186.html', 'http://www.p2pjd.com/News/29185.html', 'http://www.p2pjd.com/News/29184.html', 'http://www.p2pjd.com/News/29183.html', 'http://www.p2pjd.com/News/29182.html', 'http://www.p2pjd.com/News/29181.html', 'http://www.p2pjd.com/News/29180.html', 'http://www.p2pjd.com/News/29179.html', 'http://www.p2pjd.com/News/29178.html', 'http://www.p2pjd.com/News/29177.html', 'http://www.p2pjd.com/News/29176.html', 'http://www.p2pjd.com/News/29175.html', 'http://www.p2pjd.com/News/29174.html', 'http://www.p2pjd.com/News/29173.html', 'http://www.p2pjd.com/News/29172.html', 'http://www.p2pjd.com/News/29171.html', 'http://www.p2pjd.com/News/29170.html', 'http://www.p2pjd.com/News/29169.html', 'http://www.p2pjd.com/News/29168.html', 'http://www.p2pjd.com/News/29167.html', 'http://www.p2pjd.com/News/29166.html', 'http://www.p2pjd.com/News/29165.html', 'http://www.p2pjd.com/News/29164.html', 'http://www.p2pjd.com/News/29163.html', 'http://www.p2pjd.com/News/29162.html', 'http://www.p2pjd.com/News/29161.html', 'http://www.p2pjd.com/News/29160.html', 'http://www.p2pjd.com/News/29159.html', 'http://www.p2pjd.com/News/29158.html', 'http://www.p2pjd.com/News/29157.html', 'http://www.p2pjd.com/News/28742.html', 'http://www.p2pjd.com/News/28297.html', 'http://www.p2pjd.com/News/28295.html', 'http://www.p2pjd.com/News/28250.html', 'http://www.p2pjd.com/News/28248.html', 'http://www.p2pjd.com/News/28247.html', 'http://www.p2pjd.com/News/28238.html', 'http://www.p2pjd.com/News/28227.html', 'http://www.p2pjd.com/News/28226.html', 'http://www.p2pjd.com/News/28225.html', 'http://www.p2pjd.com/News/28224.html', 'http://www.p2pjd.com/News/28212.html', 'http://www.p2pjd.com/News/28084.html', 'http://www.p2pjd.com/News/28083.html', 'http://www.p2pjd.com/News/28082.html', 'http://www.p2pjd.com/News/28081.html', 'http://www.p2pjd.com/News/28080.html', 'http://www.p2pjd.com/News/28079.html', 'http://www.p2pjd.com/News/28078.html', 'http://www.p2pjd.com/News/28077.html', 'http://www.p2pjd.com/News/27935.html', 'http://www.p2pjd.com/News/27933.html', 'http://www.p2pjd.com/News/27932.html', 'http://www.p2pjd.com/News/27931.html', 'http://www.p2pjd.com/News/27930.html', 'http://www.p2pjd.com/News/27929.html', 'http://www.p2pjd.com/News/20433.html', 'http://www.p2pjd.com/News/20219.html', 'http://www.p2pjd.com/News/20218.html', 'http://www.p2pjd.com/News/20217.html', 'http://www.p2pjd.com/News/20216.html', 'http://www.p2pjd.com/News/20215.html', 'http://www.p2pjd.com/News/20214.html', 'http://www.p2pjd.com/News/18572.html', 'http://www.p2pjd.com/News/18542.html', 'http://www.p2pjd.com/News/18232.html', 'http://www.p2pjd.com/News/18231.html', 'http://www.p2pjd.com/News/18230.html', 'http://www.p2pjd.com/News/18229.html', 'http://www.p2pjd.com/News/18228.html', 'http://www.p2pjd.com/News/18227.html', 'http://www.p2pjd.com/News/18226.html', 'http://www.p2pjd.com/News/18225.html', 'http://www.p2pjd.com/News/18224.html', 'http://www.p2pjd.com/News/18223.html', 'http://www.p2pjd.com/News/18222.html', 'http://www.p2pjd.com/News/18221.html', 'http://www.p2pjd.com/News/18220.html', 'http://www.p2pjd.com/News/18219.html', 'http://www.p2pjd.com/News/18218.html', 'http://www.p2pjd.com/News/17457.html', 'http://www.p2pjd.com/News/17456.html', 'http://www.p2pjd.com/News/17455.html', 'http://www.p2pjd.com/News/17454.html', 'http://www.p2pjd.com/News/17453.html', 'http://www.p2pjd.com/News/17452.html', 'http://www.p2pjd.com/News/17451.html', 'http://www.p2pjd.com/News/17450.html', 'http://www.p2pjd.com/News/17449.html', 'http://www.p2pjd.com/News/17448.html', 'http://www.p2pjd.com/News/17447.html', 'http://www.p2pjd.com/News/17446.html', 'http://www.p2pjd.com/News/17445.html', 'http://www.p2pjd.com/News/17444.html', 'http://www.p2pjd.com/News/17443.html', 'http://www.p2pjd.com/News/17442.html', 'http://www.p2pjd.com/News/17441.html', 'http://www.p2pjd.com/News/17440.html', 'http://www.p2pjd.com/News/17439.html', 'http://www.p2pjd.com/News/17438.html', 'http://www.p2pjd.com/News/17437.html', 'http://www.p2pjd.com/News/17436.html', 'http://www.p2pjd.com/News/17435.html', 'http://www.p2pjd.com/News/17434.html', 'http://www.p2pjd.com/News/17433.html', 'http://www.p2pjd.com/News/17432.html', 'http://www.p2pjd.com/News/17431.html', 'http://www.p2pjd.com/News/17430.html', 'http://www.p2pjd.com/News/17429.html', 'http://www.p2pjd.com/News/17428.html', 'http://www.p2pjd.com/News/17427.html', 'http://www.p2pjd.com/News/17426.html', 'http://www.p2pjd.com/News/17425.html', 'http://www.p2pjd.com/News/17424.html', 'http://www.p2pjd.com/News/17423.html', 'http://www.p2pjd.com/News/17422.html', 'http://www.p2pjd.com/News/17421.html', 'http://www.p2pjd.com/News/17420.html', 'http://www.p2pjd.com/News/17419.html', 'http://www.p2pjd.com/News/17418.html', 'http://www.p2pjd.com/News/17417.html', 'http://www.p2pjd.com/News/17416.html', 'http://www.p2pjd.com/News/17415.html', 'http://www.p2pjd.com/News/16741.html', 'http://www.p2pjd.com/News/16740.html', 'http://www.p2pjd.com/News/16739.html', 'http://www.p2pjd.com/News/15337.html', 'http://www.p2pjd.com/News/15336.html', 'http://www.p2pjd.com/News/15335.html', 'http://www.p2pjd.com/News/15334.html', 'http://www.p2pjd.com/News/15333.html', 'http://www.p2pjd.com/News/15332.html', 'http://www.p2pjd.com/News/15331.html', 'http://www.p2pjd.com/News/15330.html', 'http://www.p2pjd.com/News/15329.html', 'http://www.p2pjd.com/News/15328.html', 'http://www.p2pjd.com/News/15327.html', 'http://www.p2pjd.com/News/5810.html', 'http://www.p2pjd.com/News/5809.html', 'http://www.p2pjd.com/News/5781.html', 'http://www.p2pjd.com/News/5780.html', 'http://www.p2pjd.com/News/5713.html', 'http://www.p2pjd.com/News/5712.html', 'http://www.p2pjd.com/News/5711.html', 'http://www.p2pjd.com/News/5710.html', 'http://www.p2pjd.com/News/5709.html', 'http://www.p2pjd.com/News/5708.html', 'http://www.p2pjd.com/News/5707.html', 'http://www.p2pjd.com/News/5706.html', 'http://www.p2pjd.com/News/5705.html', 'http://www.p2pjd.com/News/5704.html', 'http://www.p2pjd.com/News/5702.html', 'http://www.p2pjd.com/News/5701.html', 'http://www.p2pjd.com/News/5700.html', 'http://www.p2pjd.com/News/5699.html', 'http://www.p2pjd.com/News/5698.html', 'http://www.p2pjd.com/News/5492.html', 'http://www.p2pjd.com/News/5490.html', 'http://www.p2pjd.com/News/5489.html', 'http://www.p2pjd.com/News/5342.html', 'http://www.p2pjd.com/News/5341.html', 'http://www.p2pjd.com/News/5340.html', 'http://www.p2pjd.com/News/5339.html', 'http://www.p2pjd.com/News/5338.html', 'http://www.p2pjd.com/News/5254.html', 'http://www.p2pjd.com/News/5253.html', 'http://www.p2pjd.com/News/5252.html', 'http://www.p2pjd.com/News/5251.html', 'http://www.p2pjd.com/News/5250.html']
    # detail_urls = ['http://www.p2pjd.com/News/34489.html']
    black_list = GetBlackList().run

    executor = ThreadPoolExecutor(max_workers=5)
    executor.map(black_list, detail_urls)


if __name__ == '__main__':
    main()
