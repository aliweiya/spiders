import requests
import re
import threading
import json

base_url = url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
}


def get_page(page):
    """
    爬去当当网页信息
    :param page: 页码
    :return: 网页信息
    """
    try:
        url = base_url + str(page)
        # print(type(url))
        response = requests.get(url=url, headers=headers)
        return response.text
    except requests.ConnectionError as e:
        print('Error', e.args)
        return None


def pase_info(item):
    """
    提取图书信息
    :param item: 网页代码
    :return: 图书信息
    """
    list_num = '<div class="list_num.*?">(.*?).</div>.*?'
    pic = '<div class="pic">.*?<a.*?>.*?<img src="(.*?)" alt=.*?>.*?</a>.*?</div>.*?'
    title = '<div class="name">.*?<a href=.*?title="(.*?)">.*?</a>.*?</div>.*?'
    biaosheng = '<div class="biaosheng">(.*?)<span>(.*?)</span></div>.*?'
    price = '<div class="price">.*?<p>.*?<span.*?class="price_n">(.*?)</span>.*?</p>.*?</div>.*?'
    pattern = re.compile('<li>.*?{}{}{}{}{}.*?</li>'.format(list_num, pic, title, biaosheng, price), re.S)
    items = re.findall(pattern, item)
    return items


def save_info(f, book):
    """
    存储到本地
    :param f: 文件对象
    :param book: 图书信息
    :return: None
    """
    # f.write(json.dumps(book, ensure_ascii=False))
    f.write(str(book))
    f.write('\n')
    f.flush()  # 强制将数据推入文件


def main(f, each):
    """
    对一整个网页信息的抓取及存储
    :param f: 文件对象
    :param each: 页码范围
    :return: None
    """
    response = get_page(each)
    book_info = pase_info(response)
    print(book_info)
    for book in book_info:
        # print(book)
        info = {
            'num': book[0],
            'pic': book[1],
            'price': book[5],
            'biaosheng': book[3] + book[4],
            'title': book[2]
        }
        print(info)
        save_info(f, info)


if __name__ == '__main__':
    MIN_PAGE = 1  # 起始页数
    MAX_PAGE = 25  # 最大页数
    f = open('当当图书.txt', 'w', encoding='utf-8')
    for each in range(MIN_PAGE, MAX_PAGE + 1):
        print('第 %s 页' % each)
        # 不能采用多线程，会保存乱序
        # th = threading.Thread(target=main, args=[each])
        # th.start()
        main(f, each)
    f.close()


